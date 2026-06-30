import streamlit as st
import pandas as pd
import numpy as np
import joblib
import tensorflow as tf
import matplotlib.pyplot as plt
import seaborn as sns
import shap

st.set_page_config(page_title="AI-Based NIDS", layout="wide")

# ── Load artifacts ──────────────────────────────────────────────
@st.cache_resource
def load_artifacts():
    rf_model = joblib.load('models/random_forest_model.pkl')
    xgb_model = joblib.load('models/xgboost_model.pkl')
    cnn_model = tf.keras.models.load_model('models/cnn_lstm_model.keras')
    scaler = joblib.load('models/scaler.pkl')
    target_encoder = joblib.load('models/target_encoder.pkl')
    feature_names = joblib.load('models/feature_names.pkl')
    return rf_model, xgb_model, cnn_model, scaler, target_encoder, feature_names

rf_model, xgb_model, cnn_model, scaler, target_encoder, feature_names = load_artifacts()
class_names = list(target_encoder.classes_)

# ── Sidebar ──────────────────────────────────────────────────────
st.sidebar.title("⚙️ Settings")
model_choice = st.sidebar.selectbox(
    "Choose Detection Model",
    ["XGBoost (Best)", "Random Forest", "CNN-LSTM"]
)
st.sidebar.markdown("---")
st.sidebar.markdown("**Project:** AI-Based Network Intrusion Detection System")
st.sidebar.markdown("**Dataset:** NSL-KDD")

# ── Main UI ──────────────────────────────────────────────────────
st.title("🛡️ AI-Based Network Intrusion Detection System")
st.markdown("Upload network traffic data (CSV) to detect and classify potential intrusions.")

uploaded_file = st.file_uploader("Upload traffic CSV (NSL-KDD format, preprocessed)", type=['csv'])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader("📊 Uploaded Data Preview")
    st.dataframe(df.head())

    # Ensure correct feature columns/order
    try:
        X_input = df[feature_names].values
    except KeyError:
        st.error(f"CSV must contain these columns: {feature_names}")
        st.stop()

    X_scaled = scaler.transform(X_input)

    if st.button("🔍 Run Detection"):
        with st.spinner("Analyzing traffic..."):

            if model_choice == "XGBoost (Best)":
                preds = xgb_model.predict(X_scaled)
                probs = xgb_model.predict_proba(X_scaled)
            elif model_choice == "Random Forest":
                preds = rf_model.predict(X_scaled)
                probs = rf_model.predict_proba(X_scaled)
            else:  # CNN-LSTM
                X_cnn = X_scaled.reshape(X_scaled.shape[0], X_scaled.shape[1], 1)
                probs = cnn_model.predict(X_cnn)
                preds = np.argmax(probs, axis=1)

            pred_labels = target_encoder.inverse_transform(preds)
            confidence = np.max(probs, axis=1)

            results_df = df.copy()
            results_df['Predicted_Label'] = pred_labels
            results_df['Confidence'] = confidence.round(3)

        st.success("Detection complete!")

        # ── Results table with color highlighting ──────────────
        st.subheader("🚨 Detection Results")

        def highlight_attacks(row):
            color = 'background-color: #ffcccc' if row['Predicted_Label'] != 'Normal' else ''
            return [color] * len(row)

        st.dataframe(results_df.style.apply(highlight_attacks, axis=1))

        # ── Summary stats ────────────────────────────────────────
        col1, col2, col3 = st.columns(3)
        total = len(results_df)
        attacks = (results_df['Predicted_Label'] != 'Normal').sum()
        normal = total - attacks

        col1.metric("Total Records", total)
        col2.metric("Detected Attacks", attacks, delta=f"{attacks/total*100:.1f}%")
        col3.metric("Normal Traffic", normal, delta=f"{normal/total*100:.1f}%")

        # ── Attack type distribution chart ──────────────────────
        st.subheader("📈 Attack Type Distribution")
        fig, ax = plt.subplots(figsize=(8,4))
        results_df['Predicted_Label'].value_counts().plot(kind='bar', ax=ax, color='#2E75B6')
        ax.set_ylabel("Count")
        ax.set_xlabel("Class")
        st.pyplot(fig)

        # ── SHAP explanation for XGBoost ─────────────────────────
        if model_choice == "XGBoost (Best)":
            st.subheader("🔬 Why These Predictions? (SHAP Explainability)")
            with st.spinner("Computing SHAP values..."):
                explainer = shap.TreeExplainer(xgb_model)
                sample = X_scaled[:min(100, len(X_scaled))]
                shap_values = explainer.shap_values(sample)

                # Pick most common predicted attack class for summary
                top_class_name = results_df['Predicted_Label'].mode()[0]
                top_class_idx = list(class_names).index(top_class_name)

                fig2, ax2 = plt.subplots()
                shap.summary_plot(
                    shap_values[:, :, top_class_idx],
                    sample,
                    feature_names=feature_names,
                    show=False
                )
                st.pyplot(fig2)

        # ── Download results ─────────────────────────────────────
        csv = results_df.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Download Results CSV", csv, "nids_results.csv", "text/csv")

else:
    st.info("👆 Upload a CSV file to begin detection. The file should contain the same 41 features used during training.")

    
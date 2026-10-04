"""
Application Streamlit — Prédiction de la performance des étudiants (Regression Doc 1)
Modèle retenu : Lasso Regression avec RobustScaler et LabelEncoder
Lancement en local : streamlit run app.py
"""

import os
import joblib
import numpy as np
import streamlit as st

# ----------------------------------------------------------------------
# Configuration de la page
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="Student Performance Prediction",
    page_icon="🎓",
    layout="centered",
)

DESCRIPTION = (
    "Cette application permet d'estimer l'indice de performance d'un étudiant "
    "(Performance Index, échelle de 10 à 100) à partir de ses heures d'étude, "
    "de ses notes antérieures, de sa participation à des activités extrascolaires, "
    "de son temps de sommeil et du nombre d'examens blancs pratiqués."
)

# ----------------------------------------------------------------------
# Chargement des artefacts (mis en cache)
# ----------------------------------------------------------------------
@st.cache_resource
def load_artifacts():
    base_dir = os.path.dirname(__file__)
    model = joblib.load(os.path.join(base_dir, "best_model_reg.joblib"))
    encoder = joblib.load(os.path.join(base_dir, "encoder_reg.joblib"))
    scaler = joblib.load(os.path.join(base_dir, "scaler_reg.joblib"))
    return model, encoder, scaler


model, encoder, scaler = load_artifacts()

# ----------------------------------------------------------------------
# Fonction de prédiction simple
# ----------------------------------------------------------------------
def predict_performance(hours_studied, previous_scores, extracurricular, sleep_hours, sample_papers):
    # Encodage de la variable catégorielle à partir de l'encodeur sauvegardé
    extra_enc = encoder.transform([extracurricular])[0]
    
    # Vecteur des valeurs brutes dans l'ordre exact du dataset d'entraînement
    raw_vector = np.array([[hours_studied, previous_scores, extra_enc, sleep_hours, sample_papers]])
    
    # Mise à l'échelle via RobustScaler
    scaled_vector = scaler.transform(raw_vector)
    
    # Prédiction avec le modèle Lasso retenu
    pred = model.predict(scaled_vector)[0]
    
    # Bornage logique entre 10 et 100 (échelle du dataset)
    pred_bounded = max(10.0, min(100.0, float(pred)))
    return round(pred_bounded, 2)


# ----------------------------------------------------------------------
# Interface utilisateur
# ----------------------------------------------------------------------
st.title("🎓 Student Performance Prediction")
st.write(DESCRIPTION)

with st.form("form_single_prediction"):
    col1, col2 = st.columns(2)
    with col1:
        hours_studied = st.number_input(
            "Hours Studied (Heures d'étude)",
            min_value=1.0,
            max_value=9.0,
            value=5.0,
            step=1.0,
            format="%.1f",
        )
        previous_scores = st.number_input(
            "Previous Scores (Score antérieur, /100)",
            min_value=40.0,
            max_value=99.0,
            value=70.0,
            step=1.0,
            format="%.1f",
        )
        extracurricular = st.selectbox(
            "Extracurricular Activities (Activités extrascolaires)",
            options=list(encoder.classes_),
        )
    with col2:
        sleep_hours = st.number_input(
            "Sleep Hours (Heures de sommeil)",
            min_value=4.0,
            max_value=9.0,
            value=7.0,
            step=1.0,
            format="%.1f",
        )
        sample_papers = st.number_input(
            "Sample Question Papers Practiced (Examens blancs)",
            min_value=0.0,
            max_value=9.0,
            value=3.0,
            step=1.0,
            format="%.1f",
        )

    submit_btn = st.form_submit_button("Prédire la performance", type="primary")

if submit_btn:
    try:
        score_predit = predict_performance(
            hours_studied, previous_scores, extracurricular, sleep_hours, sample_papers
        )
        st.success(f"🎯 **Performance Index estimé : {score_predit} / 100**")
    except Exception as e:
        st.error(f"Erreur lors de la prédiction : {e}")

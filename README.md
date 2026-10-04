# Déploiement : Prédiction de la Performance des Étudiants (Regression Doc 1)

Cette application interactive Streamlit permet d'estimer l'indice de performance d'un étudiant (`Performance Index`, borné entre 10 et 100) à partir de caractéristiques d'apprentissage et de comportement.

## Modèle retenu et artefacts
- **Modèle final :** Lasso Regression (`best_model_reg.joblib`), sélectionné comme modèle le plus performant et régularisé (meilleur MSE et $R^2 = 0.989$ sur la validation).
- **Mise à l'échelle :** `RobustScaler` (`scaler_reg.joblib`).
- **Encodage catégoriel :** `LabelEncoder` (`encoder_reg.joblib`) pour la variable `Extracurricular Activities` (`['No', 'Yes']`).

## Variables en entrée
1. `Hours Studied` : Nombre d'heures d'étude par semaine (1 à 9).
2. `Previous Scores` : Score moyen antérieur (/100, 40 à 99).
3. `Extracurricular Activities` : Participation à des activités extrascolaires (`No` ou `Yes`).
4. `Sleep Hours` : Nombre moyen d'heures de sommeil (4 à 9).
5. `Sample Question Papers Practiced` : Nombre de devoirs d'entraînement pratiqués (0 à 9).

## Lancement en local
```bash
cd "Rendu/Supervised/Regression/Doc 1/Deployment"
streamlit run app.py
```

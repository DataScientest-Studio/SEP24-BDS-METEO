import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, recall_score, f1_score, precision_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

import xgboost as xgb
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
from keras.optimizers import Adam


from page_modelisation_multi import models_multi_days

RANDOM_STATE = 2406


def page_modelisation():
    st.header(":blue[6- Modélisation]")
    st.write("### :green[Choix des approaches]")
    st.write("""Deux options sont possibles, analyser uniquement aujourd'hui pour prédire le jour de demain ou analyser l'historique de plusieurs jours.\
             Les deux approaches ont été étudiés""")

    st.write("### :green[Modélisation des Modèles Machine Learning et Deep Learning]")

    architecture = st.selectbox(label="Choisissez type d'architecture globale", 
                                options=['Journée unique', 'Séries Temporelles'],
                                index=0)
    
    if architecture == "Journée unique":
        models_unique_day()
    elif architecture == "Séries Temporelles":
        models_multi_days()

def models_unique_day():
    # Désactiver les options spécifiques à OneDNN pour TensorFlow
    os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

    X_train, X_test, y_train, y_test = load_data()

    # Identification des colonnes numériques et catégorielles
    num_features = X_train.select_dtypes(include=["float64", "int64"]).columns
    cat_features = X_train.select_dtypes(include=["object"]).columns

    # Préprocesseur pour normalisation et encodage
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), num_features),
            ("cat", OneHotEncoder(drop="first"), cat_features),
        ]
    )

    # Organisation avec des colonnes
    col1, col2 = st.columns([1, 2])

    with col1:
        st.write("#### :green[Choix des Modèles et Paramètres]")
        model_options = ["Logistic Regression", "Random Forest", "XGBoost", "LSTM"]
        model_choice = st.selectbox("Choisissez un modèle :", model_options)

        # Hyperparamètres spécifiques
        if model_choice == "Logistic Regression":
            C = st.slider("C (inverse régularisation)", 0.01, 10.0, 1.0)
            max_iter = st.slider("Nombre max d'itérations", 100, 2000, 1000)

        elif model_choice == "Random Forest":
            n_estimators = st.slider("Nombre d'arbres", 50, 300, 100, 50)
            max_depth = st.slider("Profondeur max", 5, 50, 10, 5)

        elif model_choice == "XGBoost":
            n_estimators = st.slider("Nombre d'arbres", 50, 300, 100, 50)
            max_depth = st.slider("Profondeur max", 3, 10, 6)
            learning_rate = st.slider("Taux d'apprentissage", 0.01, 0.5, 0.1)

        else:  # LSTM
            lstm_units = st.slider("Nombre d'unités LSTM", 10, 100, 20, 10)
            dropout_rate = st.slider("Taux de Dropout", 0.1, 0.5, 0.2, 0.1)
            epochs = st.slider("Nombre d'époques", 10, 100, 30, 10)
            batch_size = st.slider("Taille de batch", 16, 128, 64, 16)
    
        if st.button("Lancer le modèle"):
            with col2:
                st.write("#### :green[Résultats]")
                results = {}


                if model_choice == "Logistic Regression":
                    model = LogisticRegression(C=C, max_iter=max_iter, random_state=42)
                elif model_choice == "Random Forest":
                    model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=42)
                elif model_choice == "XGBoost":
                    model = xgb.XGBClassifier(
                        n_estimators=n_estimators, max_depth=max_depth, learning_rate=learning_rate, random_state=42
                    )
                else:  # LSTM
                    X_train_processed = preprocessor.fit_transform(X_train)
                    X_test_processed = preprocessor.transform(X_test)
                    timesteps, features = 1, X_train_processed.shape[1]
                    X_train_lstm = X_train_processed.reshape((X_train_processed.shape[0], timesteps, features))
                    X_test_lstm = X_test_processed.reshape((X_test_processed.shape[0], timesteps, features))

                    model = Sequential([
                        LSTM(lstm_units, input_shape=(timesteps, features), return_sequences=True),
                        Dropout(dropout_rate),
                        LSTM(lstm_units, return_sequences=False),
                        Dropout(dropout_rate),
                        Dense(1, activation='sigmoid')
                    ])
                    model.compile(optimizer=Adam(learning_rate=0.001), loss='binary_crossentropy', metrics=['accuracy'])
                    model.fit(X_train_lstm, y_train, epochs=epochs, batch_size=batch_size, validation_split=0.2, verbose=0)
                    results["Accuracy"] = model.evaluate(X_test_lstm, y_test, verbose=0)[1]
                    results["Recall (1)"] = recall_score(y_test, (model.predict(X_test_lstm) > 0.5).astype(int))
                    results["F1 Score"] = f1_score(y_test, (model.predict(X_test_lstm) > 0.5).astype(int))
                    results["Precision (1)"] = precision_score(y_test, (model.predict(X_test_lstm) > 0.5).astype(int))

                if model_choice != "LSTM":
                    pipeline = Pipeline(steps=[("preprocessor", preprocessor), ("model", model)])
                    pipeline.fit(X_train, y_train)
                    y_pred = pipeline.predict(X_test)
                    results["Accuracy"] = accuracy_score(y_test, y_pred)
                    results["Recall (1)"] = recall_score(y_test, y_pred)
                    results["F1 Score"] = f1_score(y_test, y_pred)
                    results["Precision (1)"] = precision_score(y_test, y_pred)

                # Affichage des résultats
                st.write(pd.DataFrame([results], index=["Metrics"]))
                st.bar_chart(results)

@st.cache_data
def load_data():
    dataset = pd.read_csv("data/dataset.csv", encoding="utf-8")
    X = dataset.drop(columns=["RainTomorrow", "Unnamed: 0"], errors="ignore")
    y = dataset["RainTomorrow"]
    return train_test_split(X, y, test_size=0.2, random_state=42)
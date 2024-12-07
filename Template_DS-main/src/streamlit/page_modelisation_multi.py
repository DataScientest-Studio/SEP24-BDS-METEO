import pandas as pd
import numpy as np
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, recall_score, f1_score, precision_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import SMOTE

import xgboost as xgb
from keras.models import  Model
from keras.layers import LSTM, Dense, Dropout, Input, Flatten, Conv1D
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping, ReduceLROnPlateau

import os
import gzip
import shutil


RANDOM_STATE = 2406

def models_multi_days():
    sequence_length = st.slider(label="Nombre de jours à considérer",
                    min_value=2,
                    max_value=10,
                    value=5,
                    step=1)
    col1, col2 = st.columns([1, 2])

    with col1:
        st.write("#### :green[Choix des Modèles et Paramètres]")
        X, y = load_data_multi(sequence_length)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=RANDOM_STATE, shuffle=True)
        X_train, y_train = get_oversampling_serie(X_train, y_train)

        model_options = ["Logistic Regression", "Random Forest", "XGBoost", "Dense Networks","Convolutional Networks", "LSTM"]
        model_choice = st.selectbox("Choisissez un modèle :", model_options, index=1)

        if model_choice == "Logistic Regression":
            C = st.slider("C (inverse régularisation)", 0.01, 10.0, 1.0)
            max_iter = st.slider("Nombre max d'itérations", 100, 2000, 1000)
            model = LogisticRegression(C=C, max_iter=max_iter, verbose=1)

        elif model_choice == "Random Forest":
            n_estimators = st.slider("Nombre d'arbres", 50, 500, 100, 50)
            max_depth=None
            if st.checkbox("Spécifier Max_depth"):
                max_depth = st.slider("Profondeur max", 5, 50, 10, 5)
            else:
                max_depth=None
            model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=RANDOM_STATE, verbose=1, n_jobs=-1)

        elif model_choice == "XGBoost":
            n_estimators = st.slider("Nombre d'arbres", 50, 300, 100, 50)
            max_depth=None
            if st.checkbox("Spécifier Max_depth"):
                max_depth = st.slider("Profondeur max", 5, 50, 10, 5)
            else:
                max_depth=None
            learning_rate = st.slider("Taux d'apprentissage", 0.01, 0.5, 0.1)
            model = xgb.XGBClassifier(n_estimators=n_estimators, max_depth=max_depth, learning_rate=learning_rate, random_state=RANDOM_STATE)

        elif model_choice == "Dense Networks":
            deep = st.slider("Profondeur du modèle", 0, 3, 2, 1)

            hidden_layers = []
            for i in range(deep):
                hidden_layers.append(st.number_input(f"Nombre d'unités layer {i+1}", 1, None, 64, 1))
            
            model = get_dense_model(attributes=X.shape[-1],
                                    sequence_length=sequence_length,
                                    hidden_layers=hidden_layers)
            
            epochs = st.slider("Nombre d'époques", 10, 100, 30, 10)
            batch_size = st.slider("Taille de batch", 16, 128, 64, 16)

        elif model_choice == "Convolutional Networks":
            deep = st.slider("Profondeur du modèle", 0, 3, 2, 1)

            hidden_layers = []
            for i in range(deep):
                hidden_layers.append(st.number_input(f"Nombre d'unités layer {i+1}", 1, None, 64, 1))
            
            filters_conv = st.number_input("Convolutional 1D filters", 1, None, 32, 1)
            conv_length = st.number_input("Convolution 1D kernel size", 1, sequence_length, 1,1)
            dropout_rate = st.slider("Taux de Dropout", 0.1, 0.5, 0.2, 0.1)

            model = get_conv_dense_model(attributes=X.shape[-1],
                                         sequence_length=sequence_length,
                                         hidden_layers=hidden_layers,
                                         dropout=dropout_rate,
                                         filters=filters_conv,
                                         conv_seq=conv_length)
            
            
            epochs = st.slider("Nombre d'époques", 10, 100, 30, 10)
            batch_size = st.slider("Taille de batch", 16, 128, 64, 16)

        elif model_choice == "LSTM":
            lstm_units = st.number_input("Nombre d'unités LSTM", 1, None, 32, 1)

            deep = st.slider("Profondeur du modèle", 0, 3, 0, 1)

            hidden_layers = []
            for i in range(deep):
                hidden_layers.append(st.number_input(f"Nombre d'unités layer {i+1}", 1, None, 64, 1))

            model = get_lstm_dense_model(attributes=X.shape[-1],
                                         sequence_length=sequence_length,
                                         hidden_layers=hidden_layers,
                                         lstm_units=lstm_units)
            
            
            epochs = st.slider("Nombre d'époques", 10, 100, 30, 10)
            batch_size = st.slider("Taille de batch", 16, 128, 64, 16)

        if st.button("Lancer le modèle"):
            with col2:
                st.write("#### :green[Résultats]")

                if model_choice in ["Logistic Regression","Random Forest", "XGBoost"]:
                    X_train = X_train.reshape((X_train.shape[0], -1))
                    X_test = X_test.reshape((X_test.shape[0], -1))
                    sc = StandardScaler()
                    X_train = sc.fit_transform(X_train)
                    X_test = sc.transform(X_test)
                    print("Fitting model")
                    model.fit(X_train,y_train)
                    y_pred = model.predict(X_test)
                    results = metrics_results(y_test, y_pred)

                else:
                    earlyStopping = EarlyStopping(monitor='val_loss', patience=10, verbose=0, mode='min', restore_best_weights=True)
                    reduce_lr_loss = ReduceLROnPlateau(monitor='val_loss', factor=0.1, patience=5, verbose=1, epsilon=1e-4, mode='min')
                    print("Fitting model")
                    model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_data=(X_test, y_test), callbacks=[earlyStopping, reduce_lr_loss])
                    y_pred = model_prediction(model, X_test)
                    results = metrics_results(y_test, y_pred)

                # Affichage des résultats
                st.write(pd.DataFrame([results], index=["Metrics"]))
                st.bar_chart(results)

# Chargement des données

@st.cache_data
def load_data_multi(sequence_length=5):
    filename = f"data/dataset_serie_{sequence_length}.npz.gz"

    with gzip.open(filename, "rb") as f_in:
        filename_no_zip =  filename[:-3]
        with open(filename_no_zip, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)

    with np.load(filename_no_zip) as data:
        X_loaded = data["X"]
        y_loaded = data["Y"]

    os.remove(filename_no_zip)
    return X_loaded, y_loaded

def get_oversampling_serie(X, Y):

    smote = SMOTE(random_state=2406, n_jobs=-1)
    indexes_X = np.arange(len(Y))  # Crear un índice para rastrear secuencias
    indixes_resampled, Y_over = smote.fit_resample(indexes_X.reshape(-1, 1), Y)

    X_over = X[indixes_resampled.ravel()]
    
    return X_over, Y_over

def metrics_results(y_true, y_pred):
    results={"Accuracy": accuracy_score(y_true, y_pred),
            "Recall (1)": recall_score(y_true, y_pred),
            "F1 Score": f1_score(y_true, y_pred),
            "Precision (1)": precision_score(y_true, y_pred)}
    return results
    
def get_dense_model(attributes, 
                    sequence_length, 
                    hidden_layers:list=[64,32],
                    loss='binary_crossentropy',
                    name='model'):
    input_dense = Input(shape=(sequence_length, attributes))
    flatten_layer = Flatten()(input_dense)

    dense_layer=flatten_layer
    for units in hidden_layers:
        dense_layer = Dense(units=units, activation='relu')(dense_layer)

    output_layer = Dense(units=1, activation='sigmoid')(dense_layer)
    model_dense = Model(inputs = input_dense, outputs=output_layer, name=name)

    model_dense.compile(optimizer=Adam(learning_rate=0.0001),
                        loss=loss,
                        metrics=['accuracy'])
    return model_dense

def get_conv_dense_model(attributes, 
                         sequence_length, 
                         hidden_layers:list=[64,32],
                         filters=32,
                         dropout=0.2,
                         loss='binary_crossentropy',
                         conv_seq = 1,
                         name='model'):
    input_dense = Input(shape=(sequence_length, attributes))
    conv_1d = Conv1D(filters=filters,
                     kernel_size=(conv_seq),
                     activation='relu')(input_dense)
    flatten_layer = Flatten()(conv_1d)
    dropout = Dropout(dropout)(flatten_layer)

    dense_layer=dropout
    for units in hidden_layers:
        dense_layer = Dense(units=units, activation='relu')(dense_layer)

    output_layer = Dense(units=1, activation='sigmoid')(dense_layer)
    model = Model(inputs = input_dense, outputs=output_layer, name=name)

    model.compile(optimizer=Adam(learning_rate=0.0001),
                        loss=loss,
                        metrics=['accuracy'])
    return model

def get_lstm_dense_model(attributes, 
                         sequence_length, 
                         hidden_layers:list=[],
                         lstm_units=32,
                         loss='binary_crossentropy',
                         name='name'):
    input_dense = Input(shape=(sequence_length, attributes))
    lstm = LSTM(units=lstm_units)(input_dense)
    #flatten_layer = Flatten()(lstm)

    #dense_layer=flatten_layer
    dense_layer = lstm
    for units in hidden_layers:
        dense_layer = Dense(units=units, activation='relu')(dense_layer)

    output_layer = Dense(units=1, activation='sigmoid')(dense_layer)
    model = Model(inputs = input_dense, outputs=output_layer, name=name)

    model.compile(optimizer=Adam(learning_rate=0.0001),
                        loss=loss,
                        metrics=['accuracy'])
    return model

def model_prediction(model: Model, X, threshold=0.5, verbose=0):
    y_pred = model.predict(X, verbose=verbose)
    y_pred = np.where(y_pred>threshold, 1, 0)
    y_pred = y_pred.reshape((-1))
    return y_pred
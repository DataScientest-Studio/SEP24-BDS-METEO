import streamlit as st
import joblib
from page_modelisation import load_data as load_data_unique
from page_modelisation_multi import load_data_multi, get_oversampling_serie, metrics_results

from sklearn.model_selection import train_test_split
import pandas as pd
import requests
import os

RANDOM_STATE = 2406
SEQUENCE_LENGTH = 5

def page_test_model():
    st.header(":blue[7- Choix du modèle]")
    #st.write("Nous pouvons comparér les résultats des meilleurs modèles en fonction de l'architecture globale ")
    col1, col2 = st.columns([1, 1])

    with col1:
        resulst1 = unique_test()

    with col2:
        resulst2 = multi_test()

    results = pd.concat([resulst1, resulst2])

    st.bar_chart(results.T,
                 stack=False)


    st.write("""Ainsi, nous constatons que le modèle à un seul jour a des performances comparables avec un modèele complexe qui utilise plusieurs jours pour l'estimation. \
             Il a été jugé que l'utiliation d'un modèle plus complexe ne donne pas une gros gain en termes de performances, donc le modèle XGBoost sera utilisé pour deploiment.""")

    st.header(":blue[Test du modèle]")
    dict_url = get_url_dict()

    ville = st.selectbox("Sélectionner la ville", [*dict_url.keys()])

    col3, col4 = st.columns([1,2])
    
    with col3:
        df = get_info_data(ville, dict_url)
        st.write("#### :green[Information récupérée]")
        st.dataframe(df.T.iloc[:12,:].rename(columns={0:""}),
                    height=460)
        st.write(f"Request à partir du: \n*{dict_url[ville]}*")
        model = joblib.load("models/model_uni.joblib")
        RainTomorrow = model.predict(df)[0]
        RainTomorrow_prob = model.predict_proba(df)[0,1]
    with col4:
        st.write("#### :green[Résultats]")
        st.write("\n\n\n")
        if RainTomorrow == 1:
            st.write("#### Il va pluvoir demain :rain_cloud:")
            st.write(f"Probabilité: *{RainTomorrow_prob:.1%}*")
        else:
            st.write("##### Il ne va pas plouvoir demain :sunny: ")
            st.write(f"Probabilité de pluie: *{RainTomorrow_prob:.1%}*")


def unique_test():
    st.write("#### :green[Meilleur modèle jour unique]")
    #model, preprocessor = joblib.load("model/model_unique.joblib")
    X_train, X_test, y_train, y_test = load_data_unique()
    model = joblib.load("models/model_uni.joblib")

    y_pred = model.predict(X_test)

    results = metrics_results(y_test, y_pred)

    st.write(pd.DataFrame([results], index=["XGBoost"]))
    #st.bar_chart(results)

    return pd.DataFrame([results], index=["XGBoost"])

  
                            
def multi_test():
    st.write("#### :green[Meilleur modèle séries temporelles]")
    filename = "models/model_multi.joblib"
    if os.path.isfile(filename):
        model, preprocessor = joblib.load(filename)
    
        X_train, X_test, y_train, y_test = preprocessing_multi()
    
        X_test = preprocessor.transform(X_test)
    
        y_pred = model.predict(X_test)

        results = metrics_results(y_test, y_pred)
    else:
        results = {"Accuracy": 0.8547,
                   "Recall (1)": 0.7043,
                   "F1 Score": 0.6804,
                   "Precision (1)": 0.6581}

    st.write(pd.DataFrame([results], index=["RandomForest_5"]))
    #st.bar_chart(results)

    return pd.DataFrame([results], index=["RandomForest_5"])
    
def preprocessing_multi():
    X, y = load_data_multi(SEQUENCE_LENGTH)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=RANDOM_STATE, shuffle=True)

    X_train = X_train.reshape((X_train.shape[0], -1))
    X_test = X_test.reshape((X_test.shape[0], -1))
    
    return X_train, X_test, y_train, y_test

def get_url_dict():
    url_dict = {"Melbourne": "http://www.bom.gov.au/fwo/IDV60901/IDV60901.95936.json"}

    return url_dict

def get_info_data(ville, url_dict):
   url = url_dict[ville]
   headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"}
   response = requests.get(url, headers=headers).json()['observations']["data"][:48]
   df_data = pd.DataFrame(response)

   df_villes = pd.read_csv("data/villes.csv", sep=";")
   df_villes["Climat"].replace({ 'Aride' : 0, 'Désert': 0 , 
                  'Subtropical' : 1, 
                  'Tropical' : 2, 
                  'Tempéré' : 3}, inplace=True)
   
   columns_names = ['MinTemp', 'MaxTemp', 'Rainfall', 'WindGustDir', 'WindGustSpeed',
      'Humidity9am', 'Humidity3pm', 'Pressure9am', 'Pressure3pm', 'Temp9am',
      'Temp3pm', 'RainToday', 'Month', 'Climat', 'Latitude',
      'Longitude', 'Long_discret', 'Lati_discret', 'Discret']
   df = pd.DataFrame([], columns=columns_names)

   df.loc[0, 'MinTemp'] = df_data['air_temp'].min()
   df.loc[0, 'MaxTemp'] = df_data['air_temp'].min()
   df.loc[0, 'Rainfall'] = df_data["rain_trace"].astype("float").max()
   max_gust = df_data["gust_kmh"].max()
   df.loc[0, 'WindGustSpeed'] = max_gust
   df.loc[0, 'WindGustDir'] = df_data[df_data["gust_kmh"] == max_gust]["wind_dir"].mode()[0]

   #9:00am data
   data_9am = df_data[df_data["local_date_time"].str[-7:] == "09:00am"].reset_index().head(1)
   df.loc[0, 'Humidity9am'] = data_9am.loc[0,"rel_hum"]
   df.loc[0, 'Pressure9am'] = data_9am.loc[0, "press"]
   df.loc[0, 'Temp9am'] = data_9am.loc[0, "air_temp"]

   #3:00pm data
   data_3pm = df_data[df_data["local_date_time"].str[-7:] == "03:00pm"].reset_index().head(1)
   df.loc[0, 'Humidity3pm'] = data_3pm.loc[0,"rel_hum"]
   df.loc[0, 'Pressure3pm'] = data_3pm.loc[0, "press"]
   df.loc[0, 'Temp3pm'] = data_3pm.loc[0, "air_temp"]

   df.loc[0, 'RainToday'] = 1 if df.loc[0, "Rainfall"] >= 1 else 0
   df.loc[0, 'Month'] = df_data.loc[0, "local_date_time_full"][4:6]

   df.loc[0, 'Climat'] = df_villes[df_villes['Ville'] == ville].iloc[0,2]

   df.loc[0, "Latitude"] = df_data.loc[0, "lat"]
   df.loc[0, "Longitude"] = df_data.loc[0, "lon"]
   df.loc[0, "Long_discret"] = "E"
   df.loc[0, "Lati_discret"] = "S"
   df.loc[0, "Discret"] = "SE"
   
   cat_cols = ["WindGustDir", "Long_discret","Lati_discret", "Discret"] 
   for column in  df.columns:
      if column not in cat_cols:
         df[column] = df[column].astype(float)
   return df
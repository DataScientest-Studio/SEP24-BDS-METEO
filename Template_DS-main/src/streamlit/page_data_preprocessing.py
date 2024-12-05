import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px 
import pandas as pd


def page_data_preprocessing(df_hist, df_villes):
    st.header(":blue[4. Préprocessing]") 
    st.write("#### :blue[**4.1. Généralités**]")
    st.write("Le but de cette étape est de préparer le jeu de données pour l'étude. Cette étape passe par : ")
    st.write(" - une phase d'étude des données;")
    st.write(" - un enrichissement du dataframe à l'aide de données complémentaires;")
    st.write(" - une complétion des NA par des valeurs caculées ou déduites à partir des données existantes.")
        
    if st.checkbox("Afficher le nombre de NA par colonne") :
        fig = px.bar(x = df_hist.columns,y= df_hist.isna().mean()*100)    
        st.plotly_chart(fig)
        
    st.write("")
    st.write("Une stratégie de traitement de ces valeurs manquantes doit être définie pour :")   
    st.write(" - Garder un maximum de données;")
    st.write(" - Ne pas modifier substantiellement variables initiales.")

    st.write("#### :blue[**4.2. Création de fonction pour le pré-processing**]")
    st.write("Afin de mutualiser les traitements, nous avons créer des fonctions de complétion des données : ")
    st.write("   ***- f_add_info_location*** :  Fonction qui ajoute au dataframe les infos complémentaires sur le lieu : Climat, Longitude, Latitude,  Découpage du continent en 9 zones  ")  
    st.write("   ***- f_get_median_value*** : Fonction qui retourne la valeur médiane d'une colonne sur l'intervalle [j-3; j+3] ")  
    st.write("   ***- f_get_mean_value*** : Fonction qui retourne la valeur moyenne d'une colonne sur l'intervalle [j-3; j+3] ")     
    st.write("   ***- f_create_df_mean*** : création d'un dataframe contenant les valeurs moyennes pour une journée donnée sur un climat donné ")  
    st.write("   ***- f_maj_na_mean*** : Mise à jour des valeurs Na d'une liste de colonne à l'aide de la moyenne")  
    st.write("   ***- f_maj_na_mean*** : Mise à jour des valeurs Na d'une liste de colonne à l'aide de la médiane")  
    st.write("   ***- f_maj_humidity*** : Mise à jour des données manquantes sur le colonne Humidity. Si Raintoday = 1 , Alors Humidity = 100,   sinon  par la moyenne des humidité de la semaine pour le même clinat ")  
    st.write("   ***- f_maj_rainfall*** : Mise à jour des données manquantes sur le colonne Rainfall. Si Raintoday = 0 , Alors Rainfall = 0,  sinon  par la moyenne des rainfall de la semaine pour le même clinat ")  
    st.write("   ***- f_maj_windspeed*** : Description : Mise à jour des valeurs manquantes de la colonne WindSpeedGust par le max de WindSpeed9am et WindSpeed3pm")
    st.write("   ***- f_maj_windgustdir*** : Mise à jour des valeurs manquantes de la colonne WindGustDir par la valeur de WindGustDir3pm")
 
    
    st.write("#### :blue[**4.3. Pré-processing par colonne**]")   
    
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["Date", "Lieu", "Température", 
                                                        "Pression", "Précipitation", "Vent", "Données complémentaires"])

    with tab1: # Données Date 
        st.write ("A partir de la donnée date d'observation, nous avons créé les nouvelles colonnes :")
        st.write(" - **Year :** Année de l'observation;")
        st.write(" - **Month :** Mois de l'observation")
        st.write(" - **Day :** Jour de l'observation")
       
           
    with tab2:  # Location
        st.write("La première étape a été d'enrichir les données du dataframe avec des données complémentaires déduites à partir de la localité.")
        st.write("Les données ajoutées sont : ")
        st.write(" - Les coordonnées gégraphiques de la localité : Longitude et Latitude;")
        st.write(" - Le type de climat associé à la localité;")
        st.image('images/climat australie.jpg', caption=None, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")  
    
        if st.checkbox("Afficher le dataframe utilisé pour enrichir les données localisation") :
            st.dataframe(df_villes.head(10))
         
   
    with tab3:  # Température
        st.write("**- Temp9am  :** Remplacement des NA par la moyenne de Temp9am sur le même climat sur +/- 3 jours.")
        st.write("**- Temp3pm  :** Remplacement des NA par la moyenne de Temp3pm sur le même climat sur +/- 3 jours.")
        st.write("**- MinTemp  :** Remplacement des NA par la moyenne de MinTemp sur le même climat sur +/- 3 jours.")
        st.write("**- MaxTemp  :** Remplacement des NA par la moyenne de MaxTemp sur le même climat sur +/- 3 jours.")

   
    with tab4:  # Pression
        st.write("**- Pressure9am  :** Suppression des lignes présentant une NA pour cette valeur.")
        st.write("**- Pressure3pm  :** Suppression des lignes présentant une NA pour cette valeur.")
        
   
    with tab5:  # Pluie
        st.write("**- Rainfall :** Si RainToday = 0 alors 0 , sinon remplacement par la moyenne du groupe climat créé pour +/- 3 jours")
        st.write("**- Raintoday :** Suppression des lignes avec NA.")
        st.write("**- Raintomorrow :** C'est  la variable cible donc suppression des lignes avec NA.")
        st.write("**- Evaporation  :** Présentant plus de 50% de valeurs manquantes, suppression de la colonne")
        st.write("**- Humidity9am  :** Suppression de la colonne.")
        st.write("**- Humidity3pm  :** Si RainToday = 1 alors 100, sinon affectation de la médiane du groupe.")
         
            
            
    with tab6:  # Vent
        st.write("**- WindGustDir :** Remplacement des NA par la direction du vent relevée à 15h.")
        st.write("**- WindGustSpeed :** Remplacement des NA par le maximum entre Windspeed9am & Windspeed3pm de la journée.")
        st.write("**- WindDir9am :** Suppression de la colonne.")
        st.write("**- WindDir3pm :** Direction du vent à 15h00.")
        st.write("**- WindSpeed9am :** Suppression de la colonne.")
        st.write("**- WindSpeed3pm :** Suppression de la colonne.")

            
            
    with tab7:  # Données Complémetaires
        st.write("**- Sunshine :** Suppression de la colonne.")
        st.write("**- Cloud9am :** Suppression de la colonne.")
        st.write("**- Cloud3pm :** Suppression de la colonne.")
        

    st.write("#### :blue[**4.4. Résultat du pré-processing**]")   
    if st.checkbox("Afficher le nombre de NA par colonne après pré-processing") :
        df_result = pd.read_csv("./../../Data/dataset.csv")
        fig = px.bar(x = df_result.columns,y= df_result.isna().mean()*100)    
        st.plotly_chart(fig)

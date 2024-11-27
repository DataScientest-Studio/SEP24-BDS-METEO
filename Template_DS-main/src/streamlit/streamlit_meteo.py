import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


df_hist = pd.read_csv("weatherAUS.csv")
df_villes = pd.read_csv("villes.csv")
st.sidebar.image("favicon.png")
st.title(":blue[Prévisions météo en Australie]")
st.sidebar.title(":blue[Sommaire]")



pages=["Introduction", "Description du jeu de données", "Préprocessing", "DataVizualization", "Modélisation", "Bibliographie"]
page=st.sidebar.radio("Aller vers", pages)


st.sidebar.title(":blue[Intervenants]")
st.sidebar.write(" - Christelle MENARD")
st.sidebar.write(" - Fabrice SERGENT")
st.sidebar.write(" - Rachid MAHDI")
st.sidebar.write(" - Sergio VELASCO")

st.sidebar.title(":blue[Tuteur :] Antoine FRADIN")

if page == pages[0] : 
    st.header(":blue[Introduction]") 
    st.write ("Cet ensemble de données contient environ 10 ans d'observations météorologiques quotidiennes provenant de nombreux endroits en Australie.")
    st.write("Le premier objectif est de prédire la variable cible : RainTomorrow. Elle signifie : a-t-il plu le jour suivant, oui ou non ? Cette colonne est Oui si la pluie pour ce jour était de 1mm ou plus.")
    st.image('australie.jpg', caption=None, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")


if page == pages[1] : 
    st.header(":blue[Description du jeu de données]") 
    st.write("#### :blue[**Le dataframe**]")

    st.write("Le Dataframe principal est composé de l'historique des données météo en Australie sur 10 ans")
    st.dataframe(df_hist.head(20)  )
    nlig, ncol = df_hist.shape
    st.write( f"Le DataFrame est composé de {nlig} lignes et {ncol} colonnes.")
    
    

    st.write("#### :blue[**Les données**]")
    st.write("Les données composant le dataframe peuvent être classées selon les typologies suivantes :")
   
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["Date", "Location", "Température", 
                                                        "Pression", "Précipitation", "Vent", "Données complémentaires"])

    with tab1: # Données Date 
        st.write("**- Date :** date d'observation des données météo")
          
    
    with tab2:  # Location
        st.write("**- Location :** lieu d'observation des données météo")
        
        # Tracé de la carte d'Australie avec les villes
        st.image('carte_villes.png', caption=None, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")

    
    with tab3:  # Température
        st.write("**- Temp9am  :** températures observées à 9h00.")
        st.write("**- Temp3pm  :** températures observées à 15h00.")
        st.write("**- MinTemp  :** températures minimale observée sur la journée.")
        st.write("**- MaxTemp  :** températures maximale observée sur la journée.")
        
        if st.checkbox("Afficher la description des colonnes températures") :
            st.dataframe(df_hist[["Temp9am", "Temp3pm", "MinTemp","MaxTemp"]].describe() )  

   
    with tab4:  # Pression
        st.write("**- Pressure9am  :** pression athmosphèrique observées à 9h00.")
        st.write("**- Pressure3pm  :** pression athmosphèrique observées à 15h00.")
        
        if st.checkbox("Afficher la description des colonnes pression athmosphèrique") :
            st.dataframe(df_hist[["Pressure9am", "Pressure3pm"]].describe() ) 
   
    with tab5:  # Pluie
        st.write("**- Rainfall :** Taux de précipitations enregistrée pour la journée en mm.")
        st.write("**- Raintoday :** Indicateur de pluie. Il a pour valeur ***Vrai*** si il a plu plus d'un millimètre le jour de l'observation.")
        st.write("**- Raintomorrow :** Indicateur de pluie. Il a pour valeur ***Vrai*** si il a plu plus d'un millimètre le lendemain de l'observation.")
        st.write("**- Evaporation  :** évaporation dite de classe A (exprimée en millimètre) observée dans les 24 heures jusqu'à 9 heures du matin")
        st.write("**- Humidity9am  :** taux d'humidité observé à 9h00.")
        st.write("**- Humidity3pm  :** taux d'humidité observé à 15h00.")
        
        if st.checkbox("Afficher la description des colonnes humidité") :
            st.dataframe(df_hist[["Rainfall", "Evaporation", "Humidity9am", "Humidity3pm"]].describe() )     
            
            
    with tab6:  # Vent
        st.write("**- WindGustDir :** Direction de la rafale de vent la plus forte dans les 24 heures jusqu'à minuit.")
        st.write("**- WindGustSpeed :** La vitesse (km/h) de la plus forte rafale de vent dans les 24 heures jusqu'à minuit.")
        st.write("**- WindDir9am :** Direction du vent à 9h00.")
        st.write("**- WindDir3pm :** Direction du vent à 15h00.")
        st.write("**- WindSpeed9am :** Vitesse du vent à 9h00.")
        st.write("**- WindSpeed3pm :** Vitesse du vent à 15h00.")

        if st.checkbox("Afficher la description des colonnes vitesse du vent") :
            st.dataframe(df_hist[["WindSpeed9am", "WindSpeed3pm", "WindGustSpeed"]].describe() )  
            
            
    with tab7:  # Données Complémetaires
        st.write("**- Sunshine :** Nombre d'heures d'ensoleillement dans la journée.")
        st.write("**- Cloud9am :** Fraction de ciel obscurcie par des nuages ​à 9h. Ceci est mesuré en « octas », qui sont une unité de huitièmes. Il enregistre combien de huitièmes du ciel sont obscurcis par les nuages.")
        st.write("**- Cloud3pm :** Fraction de ciel obscurcie par des nuages ​à 15h. Ceci est mesuré en « octas », qui sont une unité de huitièmes. Il enregistre combien de huitièmes du ciel sont obscurcis par les nuages.")
          
    
    
    
if page == pages[2] :  # Préprocessing
    st.header(":blue[Préprocessing]") 
    st.write("Le but de cet étape est de préparer le jeu de données pour l'étude. Cette étape passe par : ")
    st.write(" - une phase d'étude des données;")
    st.write(" - un enrichissement du dataframe à l'aide de données complémentaires;")
    st.write(" - une complétion des NA par des valeurs caculées ou déduites à partir des données existantes.")
    
    nlig, ncol = df_hist.shape
    st.write(f"Le dataframe est composé de {nlig} enregistrements.")
    
    st.write("#### :blue[**Etude des valeurs manquantes**]")
    st.write("Le pourcentage de valeurs manquantes par colonnes est : ") 
   
 
    fig = plt.figure(figsize = (12,8))
    plt.bar ( df_hist.columns, df_hist.isna().mean() * 100, color = 'lightblue')
    plt.xticks(rotation=75, ha='right')
    plt.title ("Poucentage de valeurs nulles par colonne")
    st.pyplot(fig)
        
    if st.checkbox("Afficher le nombre de NA par colonne") :
        df = df_hist.isna().mean() * 100
        st.dataframe(df)
        
    st.write("Quatre variables présentent de nombreuses valeurs manquantes (près de 50% pour SunShine)") 
    st.write("Une stratégie de traitement de ces valeurs manquantes doit être définie pour :")   
    st.write(" - Garder un maximum de données;")
    st.write(" - Ne pas modifier substantiellement variables initiales.")

    st.write("#### :blue[**Préprocessing**]")
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["Date", "Location", "Température", 
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
        st.image('climat australie.jpg', caption=None, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")  
    
        if st.checkbox("Afficher le dataframe utilisé pour enrichir les données localisation") :
            st.dataframe(df_villes.head(10))
        
        st.write("**Préprocessing des données : ")
        st.write(" - **Climat :** A chaque ville, nous associerons le code climat suivant ") 
        st.write("                0 : Aride , Désert")
        st.write("                1 : Subtropical")
        st.write("                2 : Tropical")
        st.write("                3 : Tempéré") 
    
        st.write(" - **Coordonnées :** A chaque ville, nous associerons la **Longitude** et **Latitude** ") 
    
   
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
        st.write("**- Evaporation  :** Présentant plus de 50 % de valeurs manquantes, suppression de la colonne")
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
        
 


if page == pages[3] : 
    st.header(":blue[DataVizualization]")   
    st.write("Résumé de la table historique")
    st.dataframe(df_hist.describe())
    
if page == pages[4] : 
    st.header(":blue[Modélisation]")   
    
    
if page == pages[5] : 
    st.header(":blue[Bibliographie]")   

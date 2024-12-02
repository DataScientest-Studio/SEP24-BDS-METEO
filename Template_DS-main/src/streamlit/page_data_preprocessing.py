import streamlit as st
import matplotlib.pyplot as plt

def page_data_preprocessing(df_hist, df_villes):
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
        st.image('images/climat australie.jpg', caption=None, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")  
    
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
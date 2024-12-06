import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import plotly.graph_objects as go

def graph_hisplot(df, list_col, list_label) :
 ###########################################################################################
 ##
 ##     Tracé des histogrammes de distribution d'une liste de variables
 ##
 ###########################################################################################   
    i = 1
    
    fig = plt.figure(figsize = (20, 10))
    
    for col, label in zip(list_col, list_label) : 
        plt.subplot(2, 4, i)
        i += 1
        sns.histplot(x=df[col], kde = True, color = 'g')
        plt.title(label)
        plt.yticks([])        
        plt.ylabel("Densité")
        plt.xlabel("")

    st.pyplot(fig)
    return

def graph_boxplot(df, list_col, list_label) :
 ###########################################################################################
 ##
 ##     Tracé des boites à moustaches d'une liste de variables    
 ##
 ###########################################################################################   
    i = 1
    
    fig = plt.figure(figsize = (20, 10))
    
    for col, label in zip(list_col, list_label) : 
        plt.subplot(2, 4, i)
        i += 1
        sns.boxplot(x=df[col], color = 'g')
        plt.title(label)
        plt.ylabel("")
        plt.xlabel("")

    st.pyplot(fig)
    return        

def get_lieblle_graph_temp(option):
 ###########################################################################################
 ##
 ##     Création en dynamique du libellé du graphe présentant la température et sa moyenne associée    
 ##
 ###########################################################################################   
    ch = "Températures prélevées à {} dans la station {} du {} au {}, climat associé est {}"
    

    if option == "BadgerysCreek":
        heure = "15h00"
        datedeb = "01/01/2011"
        datefin = "30/03/2011"
        climat = "Tempéré"

    elif option == 'Canberra':
        heure = "9h00"
        datedeb = "01/11/2011"
        datefin = "31/01/2012"
        climat = "Tempéré"    
        
    elif option == 'MountGinini':
        heure = "15h00"
        datedeb = "01/01/2009"
        datefin = "28/02/2009"
        climat = "Subtropical"   
         
    elif option == 'Ballarat':
        heure = "9h00"
        datedeb = "01/05/2013"
        datefin = "31/072013"
        climat = "Tempéré"
        
    elif option == 'PearceRAAF':
        heure = "15h00"
        datedeb = "01/09/2014"
        datefin = "30/11/2014"
        climat = "Tempéré"    
        
    libelle = ch.format(heure, option, datedeb, datefin, climat)
    
    return libelle      
  
 ###########################################################################################
 ##
 ##    PROGRAMME PRINCIPAL de la page PRE PROCESSING   
 ##
 ###########################################################################################   

def page_data_preprocessing(df_hist, df_villes):    
    st.header(":blue[4. Préprocessing]") 
    st.write("#### :blue[**4.1. Généralités**]")
    st.write("Le but de cette étape est de préparer le jeu de données pour l'étude. Cette étape passe par : ")
    st.write(" - une phase d'étude des données (recherche de doublons, de valeurs aberrantes);")
    st.write(" - un enrichissement du dataframe à l'aide de données complémentaires;")
    st.write(" - une recherche des valeurs aberrantes, pour soit les corriger, soit les supprimer si la correction n'est pas aisée.")  
    st.write(" - une complétion des NA par des valeurs caculées ou déduites à partir des données existantes.")
        
    st.write("")
    st.write("Une stratégie de traitement de ces valeurs manquantes doit être définie pour :")   
    st.write(" - Garder un maximum de données;")
    st.write(" - Ne pas modifier substantiellement variables initiales.")

 
    
    st.write("#### :blue[**4.3. Pré-processing par colonne**]")   
    
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["Date", "Lieu", "Température", 
                                                        "Pression", "Précipitation", "Vent", "Données complémentaires"])

    with tab1: # Données Date 
        st.write("La date exacte du relevé n'a de valeur ajouté que dans l'etude de serie temporelle, notre étude se faisant sur des prédiction journalière.")
        
        st.write ("A partir de la donnée date d'observation, nous avons créé les nouvelles colonnes :")
        st.write(" - **Year :** Année de l'observation;")
        st.write(" - **Month :** Mois de l'observation")
        st.write(" - **Day :** Jour de l'observation")
       
           
    with tab2:  # Location
        st.write("La première étape a été d'enrichir les données du dataframe avec des données complémentaires déduites à partir de la localité.")
        
        st.write("A partir du nom des stations de météo, nous avons à l'aide de GoogleMaps et de Wikipédia, créé un datframe contenant les coordonnées GPS du lieu de relevé et le climat associé à la station.")
        st.image('images/wiki_maps.png', caption=None, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto") 
        st.write("Les données ajoutées sont : ")
        st.write(" - Les coordonnées gégraphiques de la localité : Longitude et Latitude;")
        st.write(" - Le type de climat associé à la localité;")
        st.image('images/climat australie.jpg', caption=None, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")  
    
        st.write(" - Discrétisation de la longitude (Ouest, Centre, Est) et de la latitude (Nord, Centre, Sud);")
        st.image('images/decoupage_australie.png', caption=None, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")  
        
        
        # Affichage de la distribution de températures   
        if st.checkbox("Afficher le dataframe utilisé pour enrichir les données localisation") :
            st.dataframe(df_villes.head(10))     
         
   
    with tab3:  # Température
        list_col = ["Temp9am", "Temp3pm", "MinTemp", "MaxTemp"]
        list_label = ["Température à 9h", "Température à 3h", "Température minimale", "Température maximale"]
        st.write("Les températures relevées suivent une loi normale et les boites à moustaches ne font appaitre aucune valeur aberrante ou extreme. Il n'y a donc pas de relevé de température à corriger. ")
        if st.checkbox("Afficher la distribution des températures") :
            st.image('images/distri_temperature.png', caption=None, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")   
            
        st.write("Comme la température est une donnée plutot stable, nous avons décidé de compléter les valeurs absentes sur les colonnes températures par la moyenne à +/- 3 jours sur le même climat.")
        
        df_temperature = pd.read_csv("data/df_exemple_temp.csv")
        
        choix = ['BadgerysCreek', 'Canberra', 'MountGinini', 'Ballarat', 'PearceRAAF']
        
        option = st.selectbox('Exemple : ', choix)
                       
        df_temp = df_temperature.loc[(df_temperature["Location"] == option)]

        fig = go.Figure(go.Scatter( x = df_temp['Date'],
            y = df_temp['Tempreal'], 
            name = "Température réelle"))

        fig = fig.add_trace(go.Scatter( x = df_temp['Date'],
            y = df_temp['Tempmean'],
            name = "Température moyenne"))

        fig.update_layout(
            title = get_lieblle_graph_temp(option),
            xaxis_tickformat = '%d %B %Y')
        
        st.plotly_chart(fig)



   
    with tab4:  # Pression
        st.write("Les pressions relevées suivent une loi normale et les boites à moustaches ne font appaitre aucune valeur aberrante ou extreme.")
        
        if st.checkbox("Afficher la distribution de la pression") :
            st.image('images/distri_pression.png', caption=None, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")   


        st.write("La donnée Pression étant une donnée très volatile, nous n'avons pu définir une règle de remplissage des NA, nous avons donc décider de supprimer les NA pour cette donnée.")

   
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
        
        
    st.write("#### :blue[**4.2. Création de fonction pour le pré-processing**]")
    st.write("Afin de mutualiser les traitements, nous avons créer des fonctions de complétion des données; ")
    if st.checkbox("Afficher la liste des fonctions créées") :
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


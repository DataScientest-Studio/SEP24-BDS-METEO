##############################################################################################
##
##        Import des librairies
##
##############################################################################################
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def insert_image(nom_image):
    ###########################################################################################
    ##
    ##     Insertion d'une image dans la page  
    ##
    ###########################################################################################   
    st.image(nom_image, caption=None, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")
    return

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

def get_libelle_graph_temp(option) :
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
    # Lecture des données
    df_temperature = pd.read_csv("data/df_exemple_temp.csv")
    df_dir_vent = pd.read_csv("data/df_stat_vent.csv")
    
    
    st.header(":blue[4 - Préprocessing]") 
    st.write("#### :green[**a - Généralités**]")
    insert_image("images\data_processing.jpg")
    st.write("Le but de cette étape est de préparer le jeu de données pour la création des modèles de prédiction. Cette étape passe par : ")
    st.write(" - une phase d'étude des données (recherche de doublons, étude de la répartition);")
    st.write(" - un enrichissement du dataframe à l'aide de données complémentaires;")
    st.write(" - une recherche des valeurs aberrantes, pour soit les corriger, soit les supprimer si la correction n'est pas aisée.")  
    st.write(" - une complétion des NA par des valeurs caculées ou déduites à partir des données existantes.")
        
    st.write("")
    st.write("")
    st.write("Une stratégie de traitement de ces valeurs manquantes doit être définie pour :")   
    st.write(" - Garder un maximum de données;")
    st.write(" - Ne pas modifier substantiellement la valeur des variables initiales.")

    st.write("")
    st.write("")  
    st.write("#### :green[**b - Pré-processing par colonne**]")   
    
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["Date", "Lieu", "Température", 
                                                        "Pression", "Précipitation", "Vent", "Données complémentaires"])

    with tab1: # Données Date 
        ######################################################################################################################################################
        ##
        ##  DONNEES DATES
        ##
        ######################################################################################################################################################
        st.write("La date exacte du relevé n'a de valeur ajouté que dans l'etude de serie temporelle, notre étude se faisant sur des prédiction journalière.")
        
        st.write ("A partir de la donnée date d'observation, nous avons créé les nouvelles colonnes :")
        st.write(" - **Year :** Année de l'observation;")
        st.write(" - **Month :** Mois de l'observation")
        st.write(" - **Day :** Jour de l'observation")
       
           
    with tab2:  # Location
        ######################################################################################################################################################
        ##
        ##  DONNEES LOCATION
        ##
        ######################################################################################################################################################
        st.write("La première étape a été d'enrichir les données du dataframe avec des données complémentaires déduites à partir de la localité.")
        
        st.write("A partir du nom des stations de météo, nous avons à l'aide de GoogleMaps et de Wikipédia, créé un datframe contenant les coordonnées GPS du lieu de relevé et le climat associé à la station.")
        insert_image('images/wiki_maps.png')
        st.write("Les données ajoutées sont : ")
        st.write(" - Les coordonnées gégraphiques de la localité : Longitude et Latitude;")
        st.write(" - Le type de climat associé à la localité;")
        insert_image('images/climat australie.jpg')  
    
        st.write(" - Discrétisation de la longitude (Ouest, Centre, Est) et de la latitude (Nord, Centre, Sud);")
        insert_image('images/decoupage_australie.png')  
        
        
        # Affichage de la distribution de températures   
        if st.checkbox("Afficher le dataframe utilisé pour enrichir les données localisation") :
            st.dataframe(df_villes.head(10))     
         
   
    with tab3:  # Température
        ######################################################################################################################################################
        ##
        ##  DONNEES TEMPERATURE
        ##
        ######################################################################################################################################################
        list_col = ["Temp9am", "Temp3pm", "MinTemp", "MaxTemp"]
        list_label = ["Température à 9h", "Température à 3h", "Température minimale", "Température maximale"]
        st.write("Les températures relevées suivent une loi normale et les boites à moustaches ne font appaitre aucune valeur aberrante ou extreme. Il n'y a donc pas de relevé de température à corriger. ")
        if st.checkbox("Afficher la distribution des températures") :
            insert_image('images/distri_temperature.png')   

        
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
            title = get_libelle_graph_temp(option),
            xaxis_tickformat = '%d %B %Y')
        
        st.plotly_chart(fig)

        st.write("")
        st.write("")
        st.write("**Les décisions prises pour cette catégorie de variables sont :**")    
        st.write("Comme la température est une donnée plutot stable, nous avons décidé de compléter les valeurs absentes sur les colonnes températures par la moyenne à +/- 3 jours sur le même climat.")
        


   
    with tab4:  # Pression
        ######################################################################################################################################################
        ##
        ##  DONNEES PRESSION
        ##
        ######################################################################################################################################################
        st.write("Les pressions relevées suivent une loi normale et les boites à moustaches ne font appaitre aucune valeur aberrante ou extreme.")
        
        if st.checkbox("Afficher la distribution de la pression") :
            insert_image('images/distri_pression.png')   
        
        st.write("**Les décisions prises pour cette catégorie de variables sont :**")   
        st.write("La donnée Pression étant une donnée très volatile, nous n'avons décider de na pas définir de règle de remplissage des NA et donc décider de supprimer les NA pour cette donnée.")

   
    with tab5:  # Pluie
        ######################################################################################################################################################
        ##
        ##  DONNEES PLUIE
        ##
        ######################################################################################################################################################
        st.write("Les précipitaions relevées suivent une loi normale et les boites à moustaches ne font appaitre aucune valeur aberrante ou extreme.")
        st.write("Les courbes font apparaitre des pics de distribution à chaque dizaine, peut être est-ce due à la précision des appareils de mesures ou un arrondi utilisateur dans certaines stations.")
        if st.checkbox("Afficher la distribution de la humidité") :
            insert_image('images/distri_humidity.png')   

        st.write("Le graphique ci dessous permet de mettre en évidence qu'il y existe une corrélation enetre le nombre de joour de pluie et le type de climat")
        insert_image('images/nb_jourpluie_climat.png')   
        
        st.write("")
        st.write("")
        st.write("**Les décisions prises pour cette catégorie de variables sont :**")   
        st.write("**- Suppression des lignes avec NA :** Raintoday et Raintomorrow.")
        st.write("**- Suppression des colonnes :** Evaporation et Humidity9am")
        st.write("**- Humidity3pm  :** Si RainToday = 1 alors 100, sinon affectation de la médiane du groupe.")
        st.write("**- Rainfall :** Si RainToday = 0 alors 0 , sinon remplacement par la moyenne du groupe climat créé pour +/- 3 jours")
        
         
            
            
    with tab6:  # Vent
        ######################################################################################################################################################
        ##
        ##  DONNEES VENT
        ##
        ######################################################################################################################################################
        st.write("L'étude des données n'a fait apparaitre aucune donnée aberrante ou erronnée. Les directions des vents sont réparties de manière uniforme.")
        
        fig = make_subplots(rows=1, cols=3, specs=[[{'type': 'polar'}]*3])


        fig.add_trace(go.Scatterpolar( name = "Direction de la plus grosse rafale de vent",  r=df_dir_vent["WindGustDir"], theta=df_dir_vent["Direction"] ), 1, 1)
        fig.add_trace(go.Scatterpolar( name = "Direction du vent à 9h00",  r=df_dir_vent["WindDir9am"], theta=df_dir_vent["Direction"] ), 1, 2)
        fig.add_trace(go.Scatterpolar( name = "Direction du vent à 15h00",  r=df_dir_vent["WindDir3pm"], theta=df_dir_vent["Direction"] ), 1, 3)

        fig.update_traces(fill='toself')

        fig.update_layout(
            polar1 = dict(
            radialaxis_angle = 90,
            angularaxis = dict(
                direction = "clockwise")
            ),
            polar2 = dict(
            radialaxis_angle = 90,
            angularaxis = dict(
                direction = "clockwise")
            ),
            polar3 = dict(
            radialaxis_angle = 90,
            angularaxis = dict(
                direction = "clockwise")
            )
        )
        
        st.plotly_chart(fig)
        
        st.write("**Les décisions prises pour cette catégorie de variables sont :**")
        st.write("**- WindGustDir :** Remplacement des NA par la direction du vent relevée à 15h.")
        st.write("**- WindGustSpeed :** Remplacement des NA par le maximum entre Windspeed9am & Windspeed3pm de la journée.")
        st.write("**- Suppression des colonnes :** WindDir9am, WindSpeed9am, WindSpeed3pm.")
     
            
            
    with tab7:  # Données Complémetaires
        ######################################################################################################################################################
        ##
        ##  DONNEES COMPLEMENTAIRES
        ##
        ######################################################################################################################################################
        st.write("**- Suppression des colonnes :** Sunshine, Cloud9am, Cloud3pm.")

        
        
    st.write("#### :green[**c - Création de traitement de pré-processing**]")
    st.write("Afin de mutualiser les traitements, nous avons créer des fonctions de complétion des données.")
    if st.checkbox("Afficher la liste des fonctions créées") :
        st.write("   ***- f_add_info_location*** :  Fonction qui ajoute au dataframe les infos complémentaires sur le lieu : Climat, Longitude, Latitude,  Découpage du continent en 9 zones  ")  
        st.write("   ***- f_get_median_value*** : Fonction qui retourne la valeur médiane d'une colonne sur l'intervalle [j-3; j+3] ")  
        st.write("   ***- f_get_mean_value*** : Fonction qui retourne la valeur moyenne d'une colonne sur l'intervalle [j-3; j+3] ")     
        st.write("   ***- f_create_df_mean*** : création d'un dataframe contenant les valeurs moyennes pour une journée donnée sur un climat donné ")  
        st.write("   ***- f_maj_na_mean*** : Mise à jour des valeurs Na d'une liste de colonne à l'aide de la moyenne")  
        st.write("   ***- f_maj_na_median*** : Mise à jour des valeurs Na d'une liste de colonne à l'aide de la médiane")  
        st.write("   ***- f_maj_humidity*** : Mise à jour des données manquantes sur le colonne Humidity. Si Raintoday = 1 , Alors Humidity = 100,   sinon  par la moyenne des humidité de la semaine pour le même clinat ")  
        st.write("   ***- f_maj_rainfall*** : Mise à jour des données manquantes sur le colonne Rainfall. Si Raintoday = 0 , Alors Rainfall = 0,  sinon  par la moyenne des rainfall de la semaine pour le même clinat ")  
        st.write("   ***- f_maj_windspeed*** : Description : Mise à jour des valeurs manquantes de la colonne WindSpeedGust par le max de WindSpeed9am et WindSpeed3pm")
        st.write("   ***- f_maj_windgustdir*** : Mise à jour des valeurs manquantes de la colonne WindGustDir par la valeur de WindGustDir3pm")


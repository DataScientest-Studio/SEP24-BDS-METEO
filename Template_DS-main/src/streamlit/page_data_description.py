import streamlit as st
import plotly.express as px 
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def page_data_description(df_hist, df_villes):
    st.header(":blue[2- Description du jeu de données]") 
    st.write("##### :green[**Le dataframe**]")
    st.write("Le Dataframe principal est composé de l'**historique** des données **météo** en Australie sur **10 ans**.")
    st.dataframe(df_hist.head(20))
    nlig, ncol = df_hist.shape
       
    st.write("##### :green[**Les données**]")
    st.write(f"Il est **composé** de **{nlig}** lignes et **{ncol}** colonnes.")
    st.write("Les données composant ce dataframe peuvent être classées selon les **typologies principales** suivantes :")
   
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["Date", "Lieu", "Température", 
                                                        "Pression", "Précipitation", "Vent", "Données complémentaires"])

    with tab1: # Données Date 
        st.write("**- Date :** date d'observation des données météorologiques. Elles sont enregistrées depuis la mise en place de la station météo sur son lieu de pose. Il est à noter des dates de démarrage différentes en fonction des lieux. Certaines stations n'enregistrent pas l'ensemble des données.")
        
        fig = plt.figure()
        df_min_max_date = df_hist.groupby('Location').agg({'Date': ['min', 'max']})
        for i, location in enumerate(df_min_max_date.index):
            plt.plot([df_min_max_date.loc[location, ('Date','min')], df_min_max_date.loc[location, ('Date','max')]], [i,i], '-o');plt.yticks(range(len(df_min_max_date.index)), df_min_max_date.index)
        plt.yticks(fontsize=6);
        plt.title("Périodes des enregistrements de stations météorologiques australiennes")
        st.pyplot(fig)
       
    with tab2:  # Location
        st.write("**- Location :** lieu d'observation des données météo")
        
        # Tracé de la carte d'Australie avec les villes
        st.plotly_chart(create_map(df_villes))
        #st.image('carte_villes.png', caption=None, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")

    
    with tab3:  # Température
        st.write("**- Temp9am  :** températures observées à 9h00.")
        st.write("**- Temp3pm  :** températures observées à 15h00.")
        st.write("**- MinTemp  :** températures minimale observée sur la journée.")
        st.write("**- MaxTemp  :** températures maximale observée sur la journée.")
        
        if st.checkbox("Afficher les données statistique des colonnes températures") :
            st.dataframe(df_hist[["Temp9am", "Temp3pm", "MinTemp","MaxTemp"]].describe() )  

   
    with tab4:  # Pression
        st.write("**- Pressure9am  :** pression athmosphèrique observées à 9h00.")
        st.write("**- Pressure3pm  :** pression athmosphèrique observées à 15h00.")
        
        if st.checkbox("Afficher les données statistique des colonnes pression athmosphèrique") :
            st.dataframe(df_hist[["Pressure9am", "Pressure3pm"]].describe() ) 
   
    with tab5:  # Pluie
        st.write("**- Rainfall :** Taux de précipitations enregistrée pour la journée en mm.")
        st.write("**- Raintoday :** Indicateur de pluie. Il a pour valeur ***Vrai*** si il a plu plus d'un millimètre le jour de l'observation.")
        st.write("**- Raintomorrow :** Indicateur de pluie. Il a pour valeur ***Vrai*** si il a plu plus d'un millimètre le lendemain de l'observation.")
        st.write("**- Evaporation  :** évaporation dite de classe A (exprimée en millimètre) observée dans les 24 heures jusqu'à 9 heures du matin")
        st.write("**- Humidity9am  :** taux d'humidité observé à 9h00.")
        st.write("**- Humidity3pm  :** taux d'humidité observé à 15h00.")
        
        if st.checkbox("Afficher les données statistique des colonnes humidité") :
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


def create_map(df_villes):
    fig = px.scatter_mapbox(df_villes,
                     lat='lat',
                     lon='lng',
                     hover_name='Ville',
                     zoom=2.6,
                     center={"lat": df_villes['lat'].mean(),
                             "lon": df_villes['lng'].mean()},
                    height=600)
    fig.update_layout(mapbox_style='open-street-map')
    fig.update_layout(coloraxis_showscale=False)
    
    return fig 
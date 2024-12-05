import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px 
import seaborn as sns
from sklearn.cluster import AgglomerativeClustering

def page_data_visualization(df_hist, df_villes):
    st.header(":blue[3- DataVizualization]") 
    
    
    st.write("##### :green[**a- Analyse des valeurs manquantes**]") 
    st.write("Le dataframe est composé de 145.460 enregistrements.")
    st.write("Le nombre des valeurs manquantes par variable de ce dataframe est le suivant: ")    
    fig = plot_na_df(df_hist)
    st.pyplot(fig)    
    st.write("4 variables présentent de **nombreuses** valeurs manquantes. La **stratégie** adoptée a eu pour cible de garder un **maximum de données** tout en ne modifiant pas substantiellement les variables initiales")
    if st.checkbox("Afficher le détail des NA par colonne") :
        df = df_hist.isna().sum()
        df = df.rename("Somme")
        st.dataframe(df)    
    
    
    st.write("##### :green[**b- Analyse des corrélations**]")
    df_corr = df_hist.select_dtypes('number').corr()
    mask = np.triu(np.ones_like(df_corr, dtype=bool))        
    fig = plt.figure(figsize = (12,9))
    sns.heatmap(df_corr, annot=True, cmap='vlag', fmt='.2f', mask=mask);
    plt.title('Matrice de corrélation', fontsize=14)
    plt.xticks(rotation=75, ha='right')
    st.pyplot(fig)
    st.write("La variable cible semble être fortement corrélée aux variables : **SunShine**, **Cloud9am**, **Humidity3pm** et **Cloud3pm**.")


    st.write("##### :green[**c- Résumé des données statistiques du jeu de données**]")
    st.dataframe(df_hist.drop(columns='Date').describe())
    st.image('images/Australie_stations.jpg', caption=None, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")
    st.write("Il est à noter une disparité sur le territoire australien, du nombre de jours de pluie.")


    st.write("##### :green[**d- Conclusion**]")
    st.write("L'exploitation des données à ce niveau permet d'orienter la stratégie de préprocessing. Il nous semble en effet important de **régionaliser** les données avant d'opérer les modélisations.")




def plot_na_df(df_hist):
    fig = plt.figure(figsize = (12,8))
    plt.bar( df_hist.columns, df_hist.isna().mean()*100, color = 'green')
    plt.xticks(rotation=45, ha='right')
    plt.title ("Répartition des valeurs manquantes par colonne")
    return fig
    

#Function to create interactive maps: Not required to be used
def create_map_clusters(df_villes, n_clusters=11):
    clf = AgglomerativeClustering(n_clusters=n_clusters).fit(df_villes[['lat', 'lng']])
    labels = clf.labels_
 
    fig = px.scatter_mapbox(df_villes,
                     lat='lat',
                     lon='lng',
                     hover_name='Ville',
                     zoom=2.6,
                     center={"lat": df_villes['lat'].mean(),
                             "lon": df_villes['lng'].mean()},
                    color=labels,
                    color_continuous_scale='portland',
                    height=600)
    fig.update_layout(mapbox_style='open-street-map')
    fig.update_layout(coloraxis_showscale=False)
    
    return fig
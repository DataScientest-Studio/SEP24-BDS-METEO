import streamlit as st

import matplotlib.pyplot as plt
import plotly.express as px 

from sklearn.cluster import AgglomerativeClustering

def page_data_visualization(df_hist, df_villes):
    st.write("### DataVizualization")   
    st.write("Le dataframe est composé de 145.460 enregistrements.")
    st.write("Le nombre de valeur manquante est : ") 
    
    fig = plot_na_df(df_hist)
    st.pyplot(fig)
    
    if st.checkbox("Afficher le détail des NA par colonne") :
        df = df_hist.isna().sum()
        df = df.rename("Somme")
        st.dataframe(df)
   
    st.write("Résumé de la table historique", )
    st.dataframe(df_hist.drop(columns='Date').describe())

def plot_na_df(df_hist):
    fig = plt.figure(figsize = (12,8))
    plt.bar( df_hist.columns, df_hist.isna().sum(), color = 'lightblue')
    plt.xticks(rotation=75, ha='right')
    plt.title ("Nombre de valeurs nulles par colonne")
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
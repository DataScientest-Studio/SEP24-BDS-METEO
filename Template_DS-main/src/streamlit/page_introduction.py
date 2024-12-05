import streamlit as st

def page_introduction():
    st.header(":blue[1- Introduction]")
    st.write("##### :green[**Notre compréhension du sujet**]")
    st.write ("A la suite de **10 années** d’observations météorologiques quotidiennes, nous disposons d’un jeu de données intéressant provenant de 49 stations météorologiques en Australie.")
    st.write("##### :green[**Objectif**]")
    st.write("L'objectif est de **prédire** la météo du **lendemain** en Australie.")
    st.write("Une des variables présente dans le jeu de données(**RainTomorrow**) indique la présence de pluie le jour suivant (oui ou non).")
    st.write("Seules les hauteurs de pluie supérieures à 1mm sont considérées positives.")
    st.image('images/australie.jpg', caption=None, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")
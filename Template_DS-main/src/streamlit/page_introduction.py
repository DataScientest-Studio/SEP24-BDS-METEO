import streamlit as st

def page_introduction():
    st.write("### Introduction")
    st.write ("Cet ensemble de données contient environ 10 ans d'observations météorologiques quotidiennes provenant de nombreux endroits en Australie.")
    st.write("Le premier objectif est de prédire la variable cible : RainTomorrow. Elle signifie : a-t-il plu le jour suivant, oui ou non ? Cette colonne est Oui si la pluie pour ce jour était de 1mm ou plus.")
    st.image('images/australie.jpg', caption=None, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")
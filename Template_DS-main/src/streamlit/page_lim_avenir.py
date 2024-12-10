import streamlit as st

def page_lim_avenir():
    
    st.header(":blue[8- Conclusion et prévisions]") 
    st.write("##### :green[**Conclusion**]")
    st.write("Plusieurs modèles montrent des résultats **sensiblement équivalents** ce qui laisse penser qu'il sera **difficile** d'optimiser très notablement nos résultats. La météorologie est une science mais qui n'est malheureusement pas exacte comme ont pu nous prouver les récents évènements de Valence. Ce modèle étant basé sur les données de la veille peut donc se trouver face à un changement de situation soudain(vent, pression,...)")

    st.write("##### :green[**Prévisonnel**]")
    st.write("L'Australie est un grand pays que nous avons séparé en 9 pour optimiser notre modèle prédictif. Cependant, force est de constater que cette segmentation ne semble pas suffisante. Il pourrait être envisager de resserrer le quadrillage en fonction des typologie de climat. ")
    st.write("Nous pourrions également préconiser au gouvernement australien, l'installation de capteurs identiques et en continu sur l'ensemble de son territoire afin d'obtenir un maximum de données sur l'ensemble des variables.")
    st.write("Les variables liées aux vents pourraient être optimisées par une transformation de ces données en variables binaires ou trigonométriques ")
    st.write("Dans un objectif d’améliorer la précision, pourrait être envisagé de se mettre en relation avec l’API officielle disponible sur https://reg.bom.gov.au/climate/data/stations/ avec une fréquence de mise à jour mensuelle, quotidienne, 3h, 0.5h, 1 min.")
    

import streamlit as st

def page_metrics():
    st.header(":blue[5 -Métriques]")
    
    col1, col2 = st.columns([0.6,0.4])
    with col1:
        st.write("Nous sommes face à un problème de classification avec des données désequilibrés. Donc le choix du métrique va permettre de mieux évaluer les résultats des modèles.")
        st.write("Dans une perspective de sécurité, nous allons privilégier la détection de la pluie, donc la classification de la classe 1 (***RainTomorrow=1***)")
        st.write("La métrique **F1-Score** s'avère la plus pertinent pour mesurer la qualité de la classification.")
        _, center, __, = st.columns([0.5,2,0.3])
        with center:
            st.markdown("$$\\text{F1-Score} = 2 \\cdot \\frac{\\text{Précision} \\cdot \\text{Rappel}}{\\text{Précision} + \\text{Rappel}}$$")
        st.write("Ce choix s'explique par l'importance de concilier précision et rappel pour bien détecter les jours pluvieux.")

    with col2:
        st.image("images/class_RainTomorrow.png")

    

    metrics = st.checkbox("Rappel définitions des métriques:")
    if metrics :
        #Précision
        st.write("""**1- Précision (Precision) :**""")
        st.write("""La précision mesure la proportion des prédictions positives qui sont correctes. Elle est définie comme :""")
        st.markdown("$$\\text{Précision} = \\frac{\\text{VP}}{\\text{VP} + \\text{FP}}$$")
        st.write("""où **VP** (Vrai Positifs) correspond au nombre de cas correctement prédits comme positifs, et FP (Faux Positifs) représente le nombre de cas \
                 incorrectement prédits comme positifs. Une précision élevée signifie peu de fausses alertes.""")

        #Rappel
        st.write("""**2- Rappel (Recall) :**""")
        st.write("""Le rappel mesure la capacité du modèle à identifier les cas positifs réels. Il est défini comme :""")
        st.markdown("$$\\text{Rappel} = \\frac{\\text{VP}}{\\text{VP} + \\text{FN}}$$")
        st.write("""où **FN** (Faux Négatifs) correspond au nombre de cas positifs réels non détectés. Un rappel élevé signifie que le modèle détecte bien les cas positifs.""")

        #F1Score
        st.write("""###### 3- F1-Score :""")
        st.write("""Le F1-score est la moyenne harmonique de la précision et du rappel, ce qui permet de trouver un équilibre entre ces deux métriques. Il est défini comme :""")
        st.markdown("$$\\text{F1-Score} = 2 \\cdot \\frac{\\text{Précision} \\cdot \\text{Rappel}}{\\text{Précision} + \\text{Rappel}}$$")
        st.write("""Le F1-score est particulièrement utile lorsque les classes sont déséquilibrées ou lorsque l'on souhaite équilibrer les fausses alertes et les cas manqués.""")


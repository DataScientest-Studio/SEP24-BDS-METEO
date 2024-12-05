import streamlit as st

def page_metrics():
    st.write("### Métriques")
    st.write("""Dans ce projet académique visant à prédire la pluie du jour suivant, le choix de l'indicateur de performance s'est porté sur le F1-score \
             appliqué à la classe "RainTomorrow" (précipitations le lendemain). Ce choix s'explique par l'importance de concilier précision et rappel pour \
             bien détecter les jours pluvieux, en particulier dans une perspective de sécurité. Privilégier la détection de la pluie permet de minimiser les \
             risques associés à des événements imprévus, comme les accidents ou les perturbations, même si cela peut entraîner quelques fausses alertes.""")
    st.write("""Étant donné qu'il s'agit d'un projet académique sans client réel, cette décision a été prise selon mes propres critères, en tenant compte des \
             enjeux de sécurité et du cadre pédagogique du projet. Ce choix oriente le modèle vers une meilleure identification des jours de pluie tout en \
             maintenant une qualité équilibrée dans les prédictions.""")
    
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

import streamlit as st
import pandas as pd

#Pages scripts
from page_introduction import *
from page_data_description import *
from page_data_visualization import page_data_visualization
from page_data_preprocessing import *
from page_metrics import *
from page_modelisation import *
from page_model_test import *
from page_lim_avenir import *
from page_bibliography import *

#Data Loading
df_hist = pd.read_csv("data/weatherAUS.csv")
df_hist['Date'] = pd.to_datetime(df_hist['Date'])
df_villes = pd.read_csv("data/villes.csv", sep=';')

##Page configuration
st.set_page_config(page_title="ML - Méteo Australie",
                   layout="wide")

st.sidebar.image("images/favicon.png")
st.title(":blue[Prévisions météo en Australie]")
st.sidebar.title(":blue[Sommaire]")

pages=["1- Introduction",              #0
       "2- Description des données",   #1
       "3- DataVizualization",         #2
       "4- Preprocessing",             #3
       "5- Métriques",                 #4
       "6- Modélisation",              #5 
       "7- Test du Modèle",            #6 
       "8- Conclusion et prévisionnel",     #7
       "Bibliographie"]             #8

page=st.sidebar.radio("Aller vers", pages)

st.sidebar.title(":blue[Intervenants]")
st.sidebar.write(" - Chrystelle MENARD")
st.sidebar.write(" - Fabrice SERGENT")
st.sidebar.write(" - Rachid MAHDI")
st.sidebar.write(" - Sergio VELASCO")

st.sidebar.title(":blue[Tuteur :] Antoine FRADIN")

###Pages dévelopment
# 0-Introduction
if page == pages[0]: 
    page_introduction()

# 1-Data Description
if page == pages[1]: 
    page_data_description(df_hist, df_villes)    

# 2-Data Visualization
if page == pages[2]:
    page_data_visualization(df_hist, df_villes)

# 3-Data Preprocessing
if page == pages[3]: 
    page_data_preprocessing(df_hist, df_villes)

# 4-Metrics    
if page == pages[4]:
    page_metrics()

# 5-Modélisation      
if page == pages[5]:
    page_modelisation()

# 6-Test
if page == pages[6]:
    page_test_model()

# 7-Limitations & Avenir
if page == pages[7]:
    page_lim_avenir()

# 8-Conclusions
if page == pages[8]:
    page_conclusions()  

# 9-Bibliographie
if page == pages[9] : 
    page_bibliography()   
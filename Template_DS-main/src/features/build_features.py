###################################################################################################################
###################################################################################################################
##
##                                  IMPORT DES PACKAGES, FONCTIONS, LIBRAIRIES
## 
###################################################################################################################
###################################################################################################################
# Import des packages, librairies et fonctions
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

###################################################################################################################
###################################################################################################################
##
##                                                   FONCTIONS                                                   
##
###################################################################################################################
###################################################################################################################
def f_print (text):
    if debug : print(text)

def f_print_separateur():
    if debug : print("-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-")

def f_get_median_value(df, column:str, date, climat, range_days=3):
###################################################################################################################
##
## Fonction : f_get_median_value
## Description : Fonction qui retourne la valeur médiane d'une colonne sur l'intervalle [j-3range_days; j+range_days] 
##
## Return : Moyenne calculée
## 
###################################################################################################################    date_min = date - timedelta(days=range_days)
    date_min = date - timedelta(days=range_days)
    date_max = date + timedelta(days=range_days)
    
    ans = df[ (df['Climat'] == climat) 
                & (df['Date'] >= date_min)
                & (df['Date'] <= date_max)][column].median()
    
    return ans

def f_get_mean_value(df, colname, date, climat, range_days = 3):
###################################################################################################################
##
## Fonction : f_get_mean_value
## Description : Fonction qui retourne la valeur moyenne d'une colonne sur l'intervalle [j-3range_days; j+range_days]
## Return : Moyenne calculée
## 
###################################################################################################################
    date_min = date - timedelta(days=range_days)
    date_max = date + timedelta(days=range_days)
    
    tmp = df.loc[(df["Date"] >= date_min) & (df["Date"] <= date_max) & (df["Climat"] == climat)]

    moyenne = np.round( tmp[colname].mean(), 1) 
    return moyenne

def f_add_info_location (df):
###################################################################################################################
##
## Fonction : f_climat
## Description : Fonction qui ajoute au dataframe des infos complémentaires sur la location : 
##  Admin_name      :  Etat auquel appartient la location
##  Climat          : Climat associé à la location : 
##                          0 : Aride , Désert
##                          1 : Subtropical
##                          2 : Tropical
##                          3 : Tempéré
## 
## Latitude         : Latitude du lieu
## Longitude        : longitude du lieu
## Découpage du continent en 9 zones : 3 zones Longitudes N: Nord / C: Centre / S: Sud
##                                     3 zones Latitudes  W: Ouest / C: Centre / E: Est
##
## Return : Dataframe avec nouvelles colonnes
## 
###################################################################################################################
    f_print("f_add_info_location")
    # Import du fichiers des données complémentaires sur les villes
    df_villes = pd.read_csv(chemin_data + "villes.csv", sep=",")

    # Discretisation de la colonne Longitude
    long_discret = pd.cut(x= df_villes['Longitude'], bins= 3 , labels= ["W", "C", "E"])
    df_villes = df_villes.merge(long_discret, left_index=True, right_index=True)  

    # Discretisation de la colonne Latitude
    lat_discret = pd.cut(x= df_villes['Latitude'], bins= 3 , labels= ["S", "C", "N"])
    df_villes = df_villes.merge(lat_discret, left_index=True, right_index=True) 

    df_villes.rename({ 
                    "Longitude_x"   : "Longitude",
                    "Longitude_y"   : "Long_discret",
                    "Latitude_x"    : "Latitude",
                    "Latitude_y"    : "Lati_discret"}, 
                    inplace = True, axis= 1)
    
    df_villes["Discret"] = df_villes.apply(lambda x: x["Lati_discret"] + x["Long_discret"], axis=1)

   # Ajout des colonnes Etat et Climat
    df_new = df.merge(df_villes, left_on= 'Location', right_on= 'Ville')

    # Suppression des colonnes inutiles
    df_new = df_new.drop(columns = ['Ville', 'Country', 'Iso2', 'Capital', 'Population', 'Population_proper', 'Admin_name'], axis = 1)

    dictionnaire = { 'Aride' : 0, 'Désert': 0 , 
                    'Subtropical' : 1, 
                    'Tropical' : 2, 
                    'Tempéré' : 3}
    
    df_new["Climat"] = df_new["Climat"].replace(dictionnaire)
    df_new = df_new.astype({'Climat' : int})

    f_print_separateur()
    return df_new

def f_drop_na (df):
 ###################################################################################################################
##
## Fonction : f_drop_na
## Description : Suppression des lignes contenant des NA 
##  
## Return : df
## 
###################################################################################################################
    f_print("f_drop_na")
    # Suppression des lignes où RainTomorrow est NA
    list_col = ['RainTomorrow', 'RainToday', 'Pressure9am', 'Pressure3pm' ]
    df = df.dropna(subset = list_col)
    f_print_separateur()
    return df

def f_create_df_mean(df):
###################################################################################################################
##
## Fonction : f_create_df_mean
## Description : Création d'un dataframe contenant les moyennes par climat 
##  
## Return : df_mean
## 
###################################################################################################################
    f_print("f_create_df_mean")

    agg_dictionary = {'MinTemp': 'mean',
                    'MaxTemp': 'mean',
                    'Rainfall': 'mean',
                    'Humidity3pm': 'mean',
                    'Temp9am': 'mean',
                    'Temp3pm': 'mean'}

    df_mean = df.groupby(['Climat', 'Date']).agg(agg_dictionary).reset_index()
    f_print_separateur()

    return df_mean

def f_maj_na_mean (df):
###################################################################################################################
##
## Fonction : f_maj_na_mean (df, df_mean)
## Description : Mise à jour des valeurs manquantes par la valeur moyenne calculée
##  
## Return : df_mean
## 
###################################################################################################################
    f_print("f_maj_na_mean")

    columns_temp = ['MinTemp', 'MaxTemp', 'Temp9am', 'Temp3pm']
    for column in columns_temp:
        f_print(f"Filling column {column}")
        index_na = df[column].isna()
        f_print(f"There are {df[column].isna().sum()} missing values before filling")
        df.loc[index_na, column] = df[index_na].apply(lambda x: f_get_mean_value(df, column, x['Date'], x['Climat']), axis=1)
        f_print(f"There are {df[column].isna().sum()} after filling")
    f_print_separateur()
    return df_meteo

def f_maj_na_median(df):
###################################################################################################################
##
## Fonction : f_maj_na_median (df)
## Description : Mise à jour des valeurs manquantes par la valeur mediane calculée
##  
## Return : df_mean
## 
###################################################################################################################
    #Setting column
    column = 'Rainfall'
    f_print(f"Filling column {column}")

    #Counting missing values
    index_na = df[column].isna()
    f_print(f"There are {df[column].isna().sum()} missing values before filling")

    #Filling missing values
    df.loc[index_na, column] = df[index_na].apply(lambda x: 0 if x['RainToday'] == 0 else f_get_median_value(df, column, x['Date'], x['Climat']), axis=1)
    f_print(f"There are {df[column].isna().sum()} after filling")
    f_print_separateur()
    return df

def f_maj_humidity(df, column):
###################################################################################################################
##
## Fonction : f_maj_huldity (df)
## Description : Mise à jour des valeurs manquantes de la colonne humidity
##                  Si RainToday = 1 alors Humidity = 100 
##                                   sinon Humidity = Mediane des Humidités sur la semaine et le même Climat
## Return : df_mean
## 
###################################################################################################################
    #Setting column
  

    f_print(f"Filling column : {column}")

    f_print(f"Colonne {column}, il y a  {df[column].isna().sum()} valeurs manquantes")
    index_na = index_na = df[column].isna()

    df.loc[index_na, column] = df[index_na].apply(lambda x: 100 if x['RainToday'] == 1 else f_get_median_value(df, column, x['Date'], x['Climat']), axis=1)

    f_print(f"Colonne {column}, il y a  {df[column].isna().sum()} valeurs manquante après traitement")
    f_print_separateur()
    return df

def f_maj_rainfall(df):
###################################################################################################################
##
## Fonction : f_maj_rainfall (df)
## Description : Mise à jour des valeurs manquantes de la colonne Rainfall
##                  Si RainToday = 0 alors Rainfall = 0 
##                                   sinon Rainfall = Moyenne des rainfall sur la semaine et le même Climat
## Return : df_mean
## 
###################################################################################################################
    #Setting column
  
    column = "Rainfall"
    f_print(f"Filling column : {column}")

    f_print(f"Colonne {column}, il y a  {df[column].isna().sum()} valeurs manquantes")
    
    index_na = index_na = df[column].isna()

    df.loc[index_na, column] = df[index_na].apply(lambda x: 0 if x['RainToday'] == 0 else f_get_mean_value(df, column, x['Date'], x['Climat']), axis=1)

    f_print(f"Colonne {column}, il y a  {df[column].isna().sum()} valeurs manquante après traitement")
    f_print_separateur()
    return df

def f_maj_temperature(df, column):
###################################################################################################################
##
## Fonction : f_maj_temperature (df)
## Description : Mise à jour des valeurs manquantes des colonnes detype Température par la moyenne sur la semaine
##                 
## Return : df_mean
## 
###################################################################################################################
    f_print(f"Filling column : {column}")

    f_print(f"Colonne {column}, il y a  {df[column].isna().sum()} valeurs manquantes")

    index_na = index_na = df[column].isna()

    df.loc[index_na, column] = df[index_na].apply(lambda x: f_get_mean_value(df, column, x['Date'], x['Climat']), axis=1)

    
    f_print(f"Colonne {column}, il y a  {df[column].isna().sum()} valeurs manquante après traitement")
    f_print_separateur()
    return df

def f_maj_windspeed(df):
###################################################################################################################
##
## Fonction : f_maj_windspeed (df)
## Description : Mise à jour des valeurs manquantes de la colonne WindSpeedGust par le max de WindSpeed9am et WindSpeed3pm
##                 
## Return : df_mean
## 
###################################################################################################################
    column = "WindGustSpeed"

    f_print("f_maj_windspeed")
    f_print(f"Filling column : {column}")
    f_print(f"Colonne {column}, il y a  {df[column].isna().sum()} valeurs manquantes")

    index_na = df[column].isna()
    df.loc[index_na, column] = df[index_na].apply(lambda x: max(x['WindSpeed9am'], x['WindSpeed3pm']), axis=1)
    
    f_print(f"Colonne {column}, il y a  {df[column].isna().sum()} valeurs manquante après traitement")  
    f_print_separateur()    

    return df

def f_maj_windgustdir(df):
 ##################################################################################################################
##
## Fonction : f_maj_windgustdir (df)
## Description : Mise à jour des valeurs manquantes de la colonne WindGustDir par la valeur de WindGustDir3pm
##                 
## Return : df_mean
## 
###################################################################################################################
    column = "WindGustDir"

    f_print("f_maj_windgustdir")
    f_print(f"Filling column : {column}")
    f_print(f"Colonne {column}, il y a  {df[column].isna().sum()} valeurs manquantes")

    index_na = df[column].isna()
    df.loc[index_na, column] =  df.loc[index_na, 'WindDir3pm']
    
    f_print(f"Colonne {column}, il y a  {df[column].isna().sum()} valeurs manquante après traitement")  
    f_print_separateur()    
    return df

###################################################################################################################
###################################################################################################################
##  
##                                             PROGRAMME PRINCIPAL
##  
###################################################################################################################
###################################################################################################################

debug = False
chemin_data = "./../../data/"
# Import du fichier de données
df_meteo = pd.read_csv(chemin_data + "weatherAUS.csv")

# Découpage de la date en 3 colonnes
df_meteo['Date'] = pd.to_datetime(df_meteo['Date'], yearfirst = True)
df_meteo["Year"] = df_meteo["Date"].dt.strftime("%Y")
df_meteo["Month"] = df_meteo["Date"].dt.strftime("%m")
df_meteo["Day"] = df_meteo["Date"].dt.strftime("%d")

# Ajout des données complémentaires climat
df_meteo = f_add_info_location(df_meteo) 

# Suppression des colonnes
#   Evaportaion : nombre de NA très élevé
#   Sunshine    : Nombre de NA très élevé
df_meteo.drop(["Evaporation", "Sunshine"], axis = 1, inplace = True)
                     
# Remplacement des Yes/No par 1/0
df_meteo["RainToday"] = df_meteo["RainToday"].replace({"Yes": 1, "No": 0})
df_meteo["RainTomorrow"] = df_meteo["RainTomorrow"].replace({"Yes": 1, "No": 0})

# Création du dataframe des moyennes sur 6 jours
#df_mean = f_create_df_mean(df_meteo)

# Mise à jour des NA par la moyenne
df_meteo = f_maj_na_mean(df_meteo)

# Mise à jour des NA sur l'Humidité à 15h
df_meteo = f_maj_humidity(df_meteo, "Humidity3pm")
df_meteo = f_maj_humidity(df_meteo, "Humidity9am")

# Mise à jour des NA de RainFall
df_meteo = f_maj_rainfall(df_meteo)

# Mise à jour des variables vents
df_meteo = f_maj_windspeed(df_meteo)
df_meteo = f_maj_windgustdir(df_meteo)

# Suppression des colonnes 
df_meteo.drop(columns = ["Date", "Location", "WindDir9am", "WindDir3pm", "WindSpeed9am", "WindSpeed3pm", "Cloud9am", "Cloud3pm","Year", "Day"], 
              axis = 1, inplace = True)

# Supression des lignes aves valeurs absentes
df_meteo = f_drop_na(df_meteo)

df_meteo.to_csv(chemin_data + "dataset.csv")

input("Fin de traitement...")

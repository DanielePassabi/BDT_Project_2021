# necessary to import other modules
import sys
sys.path.append('../../application')

from functions.mysql import *
from functions.machine_learning_model import *
import pandas as pd

"""
MySQL Connection
""" 

host = "127.0.0.1"
port = 3306
database = "db_bdt_project"
user = "root"
password = "dany1998"

db_connection = connectToMySQL_Alchemy(host, port, database, user, password, False)

table = "appalti_aggiudicatari"
df = retrieveAllDataFromTable_Alchemy(table, db_connection)

print(df.head())

print("\nTotal rows:", df.shape[0])

# TEMP
print("==== TEMP ====")
df_path = "C:/Users/Daniele/Documents/Programmazione/Github/BDT_Project_2021/application/datasets/clean_data/appalti_aggiudicatari.csv"
df = pd.read_csv(df_path, sep=";")
print(df.head())
print("\nTotal rows:", df.shape[0])
print("==== TEMP ====")

create_KNeighborsClassifier(df, 1000)

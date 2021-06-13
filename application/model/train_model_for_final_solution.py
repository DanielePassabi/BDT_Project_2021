# necessary to import other modules
import sys
sys.path.append('../')

from functions.mysql import *
from functions.machine_learning_model import *
import cryptography
import pandas as pd

"""
MySQL Connection
""" 

host = "127.0.0.1"
port = 3306
database = "db_bdt_project"
user = "root"
password = "dany1998"

print("> Connecting to the database")
db_connection = connectToMySQL_Alchemy(host, port, database, user, password, False)

print("> Retrieving the data")
table = "appalti_aggiudicatari"
df = retrieveAllDataFromTable_Alchemy(table, db_connection)

print(df.head())

print("\nTotal rows:", df.shape[0])

print("> Training the model")
create_KNeighborsClassifier(df, 1000, "knn_data")
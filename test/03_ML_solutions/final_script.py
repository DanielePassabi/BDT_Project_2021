# necessary to import other modules
import sys
sys.path.append('../../application')

from functions.mysql import *

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
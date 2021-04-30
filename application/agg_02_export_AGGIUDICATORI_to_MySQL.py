from functions import *

import mysql.connector
from tqdm import tqdm
import time

################
### SETTINGS ###
################

# location of aggiudicatari .csv
agg_path = "datasets/clean_data/aggiudicatari_50k.csv"

# MySQL database
host = "127.0.0.1"
port = 3306
database = "db_bdt_project"
user = "root"
password = "dany1998"

# query information
table_name = "elenco_aggiudicatari_test"
cols_list = ["cig", "aggiudicatario", "tipo_aggiudicatario"]

##############
### SCRIPT ###
##############

# Tracking the time
start = time.time()

# Dataset import
print("\n> Importing the data from the AGGIUDICATARI .csv")
df = importAggiudicatari(agg_path)

# Establish MySQL connection
connection = connectToMySQL(host, port, database, user, password, False)
setAutocommit(connection, True)
cursor = createCursor(connection)

# execute the query
print("\n> Inserting data into", table_name)
insertDataInTable(df, cursor, table_name, cols_list)
print("> BD correctly updated")


# close the connection
closeMySQLConnection(cursor, connection)

# calculate and print total time
end = time.time()
print("\n> Elapsed time:", from_seconds_to_elapsed_time(end - start))
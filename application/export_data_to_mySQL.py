from functions import *

import mysql.connector
from tqdm import tqdm
import time

start = time.time()

print("\n> Importing the data from the .csv")

df = pd.read_csv("datasets/clean_data/full_dataset.csv", sep=";")

print("\n> Connecting to mySQL")

host = "127.0.0.1"
port = 3306
database = "db_bdt_project"
user = "root"
password = "dany1998"

print("\n>> host:", host)
print(">> port:", port)
print(">> database:", database)
print(">> user:", user)

connection = mysql.connector.connect(
    host = host,
    port = port,
    database = database,
    user = user,
    password = "dany1998"
)

print("\n> Successfully connected")

connection.autocommit = True
print("> Autocommit set to True")

cursor = connection.cursor()
query = "INSERT into appalti_aggiudicatari_test (cig, numero_gara, importo_complessivo_gara, n_lotti_componenti, importo_lotto, settore, data_pubblicazione, tipo_scelta_contraente, modalita_realizzazione, denominazione_amministrazione_appaltante, sezione_regionale, descrizione_cpv, aggiudicatario, tipo_aggiudicatario) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

print("\n> DB population started")

for i, row in df.iterrows():
    
    total_rows = df.shape[0]
    n = 1
    if (i % 50000 == 0 and i != 0):
        rows_updated = n*i
        completion_perc = round(rows_updated / total_rows, 2)
        print(">> Completed: ", completion_perc, "%")
        n = n+1

    cursor.execute(query, (row["cig"], row["numero_gara"], row["importo_complessivo_gara"], row["n_lotti_componenti"], row["importo_lotto"], row["settore"], row["data_pubblicazione"], row["tipo_scelta_contraente"], row["modalita_realizzazione"], row["denominazione_amministrazione_appaltante"], row["sezione_regionale"], row["descrizione_cpv"], row["aggiudicatario"], row["tipo_aggiudicatario"]))



print("\n> Data added to the database")

print("\n> Closing the connection")
cursor.close()
connection.close()
print("> Connection closed successfully")

end = time.time()
print("\n> Elapsed time:", from_seconds_to_elapsed_time(end - start))
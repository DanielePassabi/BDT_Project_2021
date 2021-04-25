from functions import *

import mysql.connector
from tqdm import tqdm
import time

# Tracking the time
start = time.time()

# Dataset import
print("\n> Importing the data from the CIG_AGGIUDICATARI .csv")
df = pd.read_csv("datasets/clean_data/full_dataset.csv", sep=";")

# Establish MySQL connection
host = "127.0.0.1"
port = 3306
database = "db_bdt_project"
user = "root"
password = "dany1998"

connection = connectToMySQL(host, port, database, user, password)
setAutocommit(connection, True)
cursor = createCursor(connection)

# query information
table_name = "appalti_aggiudicatari_test"
cols_list = ["cig", "numero_gara", "importo_complessivo_gara", "n_lotti_componenti", "importo_lotto", "settore", "data_pubblicazione", "tipo_scelta_contraente", "modalita_realizzazione", "denominazione_amministrazione_appaltante", "sezione_regionale", "descrizione_cpv", "aggiudicatario", "tipo_aggiudicatario"]

# execute the query
executeInsertQuery(df, cursor, table_name, cols_list)

# close the connection
closeMySQLConnection(cursor, connection)

# calculate and print total time
end = time.time()
print("\n> Elapsed time:", from_seconds_to_elapsed_time(end - start))
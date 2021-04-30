from tkinter import Tk
from tkinter.filedialog import askopenfilename

import pandas as pd

from functions import *
import time

# Tracking the time
start = time.time()

print("\n> Updating CIG AGGIUDICATARI datasets")

# Prompt the user to select a .csv
print("\n> Select the new CIG .csv")

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
cig_csv_path = askopenfilename() # show an "Open" dialog box and return the path to the selected file

cig_df = importCIG(cig_csv_path)
print("> CIG .csv correctly imported")

# Clean the CIG df
cig_df = cleanCIG(cig_df)
print("> CIG data cleaned")

# Retrieval of AGGIUDICATARI from MySQL DB
print("\n> Retrieving AGGIUDICATARI data from MySQL DB")

# 1. Establish MySQL connection
host = "127.0.0.1"
port = 3306
database = "db_bdt_project"
user = "root"
password = "dany1998"

db_connection = connectToMySQL_Alchemy(host, port, database, user, password, False)

# 2. Retrieve the AGGIUDICATARI data
table = "elenco_aggiudicatari"
agg_df = retrieveAllDataFromTable_Alchemy(table, db_connection)

print("> AGGIUDICATARI data retrieved")

# Inner Join of new CIG data and AGGIUDICATARI
print("\n> Joining CIG data with AGGIUDICATARI data")
full_df = joinCIGAggiudicatari(cig_df, agg_df)


# Add new data to MySQL appalti_aggiudicatari table

# A. create query information
table_name = "appalti_aggiudicatari_test"
cols_list = ["cig", "numero_gara", "importo_complessivo_gara", "n_lotti_componenti", "importo_lotto", "settore", "data_pubblicazione", "tipo_scelta_contraente", "modalita_realizzazione", "denominazione_amministrazione_appaltante", "sezione_regionale", "descrizione_cpv", "aggiudicatario", "tipo_aggiudicatario"]

# B. connect to db
connection = connectToMySQL(host, port, database, user, password, False)
setAutocommit(connection, True)
cursor = createCursor(connection)

# C. execute the query
print("\n> Inserting data into", table_name)
insertDataInTable(full_df, cursor, table_name, cols_list)
print("> BD correctly updated")

# D. close the connection
closeMySQLConnection(cursor, connection)

# calculate and print total time
end = time.time()
print("\n> Elapsed time:", from_seconds_to_elapsed_time(end - start))
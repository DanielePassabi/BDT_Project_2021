from functions import *

from tkinter import Tk
from tkinter.filedialog import askopenfilename
import pandas as pd
import time

"""
# This code is used to update the CIG join AGGIUDICATARI table in a MySQL DB

# 1. It prompts the user to select a (raw) CIG .csv with updated data
# 2. It cleans the new data
# 3. It retrieves the AGGIUDICATARI data from MySQL DB
# 4. It joines the new CIG data with AGGIUDICATARI data
# 5. It exports to the db the joined data
"""

################
### SETTINGS ###
################

# MySQL database
host = "127.0.0.1"
port = 3306
database = "db_bdt_project"
user = "root"
password = "dany1998"

table_agg = "elenco_aggiudicatari"
table_cig_agg = "appalti_aggiudicatari_test"
cols_list = ["cig", "numero_gara", "importo_complessivo_gara", "n_lotti_componenti", "importo_lotto", "settore", "data_pubblicazione", "tipo_scelta_contraente", "modalita_realizzazione", "denominazione_amministrazione_appaltante", "sezione_regionale", "descrizione_cpv", "aggiudicatario", "tipo_aggiudicatario"]

##############
### SCRIPT ###
##############

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
db_connection = connectToMySQL_Alchemy(host, port, database, user, password, False)

# 2. Retrieve the AGGIUDICATARI data
agg_df = retrieveAllDataFromTable_Alchemy(table_agg, db_connection)

print("> AGGIUDICATARI data retrieved")

# Inner Join of new CIG data and AGGIUDICATARI
print("\n> Joining CIG data with AGGIUDICATARI data")
full_df = joinCIGAggiudicatari(cig_df, agg_df)

# Add new data to MySQL appalti_aggiudicatari table

# A. connect to db
connection = connectToMySQL(host, port, database, user, password, False)
setAutocommit(connection, True)
cursor = createCursor(connection)

# B. execute the query
print("\n> Inserting data into", table_cig_agg)
insertDataInTable(full_df, cursor, table_cig_agg, cols_list)
print("> BD correctly updated")

# C. close the connection
closeMySQLConnection(cursor, connection)

# Calculate and print total time
end = time.time()
print("\n> Elapsed time:", from_seconds_to_elapsed_time(end - start))
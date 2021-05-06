from functions import *

from tkinter import Tk
from tkinter.filedialog import askopenfilename
import time

"""
# This code is used to update the AGGIUDICATARI table in a MySQL DB

# 1. It prompts the user to select a (raw) AGGIUDICATARI .csv with updated data
# 2. It cleans the new data
# 3. It retrieves the old AGGIUDICATARI data from MySQL DB
# 4. It compares the old data with the new one
# 5. It exports to the db the records that were not already present in the db
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

# Query information
table_name = "elenco_aggiudicatari_test"
cols_list = ["cig", "aggiudicatario", "tipo_aggiudicatario"]

##############
### SCRIPT ###
##############

# Tracking the time
start = time.time()

print("\n> Updating AGGIUDICATARI datasets")

# Prompt the user to select a .csv
print("\n> Select the new AGGIUDICATARI .csv")

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
agg_csv_path = askopenfilename() # show an "Open" dialog box and return the path to the selected file

new_agg_df = importAggiudicatari(agg_csv_path)
print("> AGGIUDICATARI .csv correctly imported")

# Clean the AGGIUDICATARI df
new_agg_df = cleanAggiudicatari(new_agg_df)
print("> AGGIUDICATARI data cleaned")

# Establish MySQL connection (alchemy)
db_connection = connectToMySQL_Alchemy(host, port, database, user, password, False)

# Retrieve the current AGGIUDICATARI data
old_agg_df = retrieveAllDataFromTable_Alchemy(table_name, db_connection)

# Find only new data
new_entries = pd.concat([old_agg_df,new_agg_df]).drop_duplicates(keep=False)

# Establish MySQL connection
connection = connectToMySQL(host, port, database, user, password, False)
setAutocommit(connection, True)
cursor = createCursor(connection)

# Inserting new AGGIUDICATARI data into the db
print("\n> Inserting new data into", table_name)
insertDataInTable(new_entries, cursor, table_name, cols_list)
print("> BD correctly updated")

# Calculate and print total time
end = time.time()
print("\n> Elapsed time:", from_seconds_to_elapsed_time(end - start))
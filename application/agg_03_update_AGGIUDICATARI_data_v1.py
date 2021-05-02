from functions import *

from tkinter import Tk
from tkinter.filedialog import askopenfilename
import time

"""
# This code is used to update the AGGIUDICATARI table in a MySQL DB

# 1. It prompts the user to select a (raw) AGGIUDICATARI .csv with updated data
# 2. It cleans the new data
# 3. It removes the old AGGIUDICATARI data from MySQL DB
# 4. It exports the new AGGIUDICATARI data into MySQL DB
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

agg_df = importAggiudicatari(agg_csv_path)
print("> AGGIUDICATARI .csv correctly imported")

# Clean the AGGIUDICATARI df
agg_df = cleanAggiudicatari(agg_df)
print("> AGGIUDICATARI data cleaned")

# Establish MySQL connection
connection = connectToMySQL(host, port, database, user, password, False)
setAutocommit(connection, True)
cursor = createCursor(connection)

# Truncate the existing AGGIUDICATARI table from MySQL db
query = "TRUNCATE `" + database + "`.`" + table_name + "`;"
cursor.execute(query)
print("\n> Table " + table_name + " correctly truncated on MySQL DB")

# Inserting new AGGIUDICATARI data into the db
print("> Inserting new data into", table_name)
insertDataInTable(agg_df, cursor, table_name, cols_list)
print("> BD correctly updated")

# Close MySQL connection
closeMySQLConnection(cursor, connection)

# Calculate and print total time
end = time.time()
print("\n> Elapsed time:", from_seconds_to_elapsed_time(end - start))
from functions import *
import time

"""
# This code is meant to be executed once
# It exports the clean .csv with all the AGGIUDICATARI data to a MySQL DB
"""

################
### SETTINGS ###
################

# Location of final AGGIUDICATARI .csv
agg_path = "datasets/clean_data/elenco_aggiudicatari_1M.csv"

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

# Final AGGIUDICATARI .csv data import
print("\n> Importing the data from the AGGIUDICATARI .csv")
df = importAggiudicatari(agg_path)

# Establish MySQL connection
connection = connectToMySQL(host, port, database, user, password, False)
setAutocommit(connection, True)
cursor = createCursor(connection)

# Execute the query
print("\n> Inserting data into", table_name)
insertDataInTable(df, cursor, table_name, cols_list)
print("> BD correctly updated")

# Close the connection
closeMySQLConnection(cursor, connection)

# Calculate and print total time
end = time.time()
print("\n> Elapsed time:", from_seconds_to_elapsed_time(end - start))
# necessary to import other modules
import sys
sys.path.append('../')

from functions.database_update import *
from config import *

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

# MySQL credentials
host = mysql_credentials["host"]
port = mysql_credentials["port"]
database = mysql_credentials["database"]
user = mysql_credentials["user"]
password = mysql_credentials["password"]

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

# Launch the update function
updateAggiudicatariTable(host, port, database, user, password, agg_csv_path)

# Calculate and print total time
end = time.time()
print("\n> Elapsed time:", from_seconds_to_elapsed_time(end - start))
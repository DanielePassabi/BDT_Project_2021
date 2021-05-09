# necessary to import other modules
import sys
sys.path.append('../')

from functions.database_update import *
from config import *

from tkinter import Tk
from tkinter.filedialog import askopenfilename
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

print("\n> Updating CIG AGGIUDICATARI datasets")

# Prompt the user to select a .csv
print("\n> Select the new CIG .csv")

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
cig_csv_path = askopenfilename() # show an "Open" dialog box and return the path to the selected file

# Launch the update function
updateCIGTable(host, port, database, user, password, cig_csv_path)

# Calculate and print total time
end = time.time()
print("\n> Elapsed time:", from_seconds_to_elapsed_time(end - start))
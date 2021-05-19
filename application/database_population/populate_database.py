# necessary to import other modules
import sys
sys.path.append('../')

from functions.database_population import *
from config import *
import time


################
### SETTINGS ###
################

# Paths
agg_dir_path = paths["agg_dir_path"]
cig_dir_path = paths["cig_dir_path"]
clean_data_dir_path = paths["clean_data_dir_path"]
clean_agg_csv_name = paths["clean_agg_csv_name"]
agg_cig_csv_name = paths["agg_cig_csv_name"]

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

# Populate the tables of the db

cleanAggiudicatari(agg_dir_path, clean_data_dir_path, clean_agg_csv_name)

# get the path of the clean AGGIUDICATARI csv
clean_agg_path = clean_data_dir_path + "/" + clean_agg_csv_name

#exportAggiudicatariToMySQL(clean_agg_path, host, port, database, user, password)

cleanCIG(cig_dir_path, clean_agg_path, clean_data_dir_path, agg_cig_csv_name)

# get the path of the clean CIG AGGIUDICATARI csv
agg_cig_csv_path = clean_data_dir_path + "/" + agg_cig_csv_name

#exportCIGAggiudicatariToMySQL(agg_cig_csv_path, host, port, database, user, password)

# Calculate and print total time
end = time.time()
print("\n\n> Elapsed time:", from_seconds_to_elapsed_time(end - start))
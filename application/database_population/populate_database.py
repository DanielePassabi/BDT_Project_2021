# necessary to import other modules
import sys
sys.path.append('../')

from functions.database_population import *
import time


################
### SETTINGS ###
################

agg_dir_path = "../datasets_test/raw_data/aggiudicatari/"   # Directory in which we find all the AGGIUDICATARI .csv
cig_dir_path = "../datasets_test/raw_data/cig/"                # Directory in which we find all the CIG .csv

clean_data_dir_path = "../datasets_test/clean_data/"        # Directory in which we store the clean data

clean_agg_csv_name = "elenco_aggiudicatari.csv"             # Name of the final AGGIUDICATARI .csv
agg_cig_csv_name = "appalti_aggiudicatari.csv"              # Name of the final CIG AGGIUDICATARI.csv

# MySQL database
host = "127.0.0.1"
port = 3306
database = "db_bdt_project"
user = "root"
password = "dany1998"

# Query information AGGIUDICATARI
agg_table_name = "elenco_aggiudicatari_test"
agg_cols_list = ["cig", "aggiudicatario", "tipo_aggiudicatario"]

# Query information CIG AGGIUDICATARI
agg_cig_table_name = "appalti_aggiudicatari_test"
agg_cig_cols_list = ["cig", "numero_gara", "importo_complessivo_gara", "n_lotti_componenti", "importo_lotto", "settore", "data_pubblicazione", "tipo_scelta_contraente", "modalita_realizzazione", "denominazione_amministrazione_appaltante", "sezione_regionale", "descrizione_cpv", "aggiudicatario", "tipo_aggiudicatario"]


##############
### SCRIPT ###
##############

# Tracking the time
start = time.time()

# Populate the tables of the db

cleanAggiudicatari(agg_dir_path, clean_data_dir_path, clean_agg_csv_name)

# get the path of the clean AGGIUDICATARI csv
clean_agg_path = clean_data_dir_path + "/" + clean_agg_csv_name

exportAggiudicatariToMySQL(clean_agg_path, host, port, database, user, password, agg_table_name, agg_cols_list)

cleanCIG(cig_dir_path, clean_agg_path, clean_data_dir_path, agg_cig_csv_name)

# get the path of the clean CIG AGGIUDICATARI csv
agg_cig_csv_path = clean_data_dir_path + "/" + agg_cig_csv_name

exportCIGAggiudicatariToMySQL(agg_cig_csv_path, host, port, database, user, password, agg_cig_table_name, agg_cig_cols_list)

# Calculate and print total time
end = time.time()
print("\n\n> Elapsed time:", from_seconds_to_elapsed_time(end - start))
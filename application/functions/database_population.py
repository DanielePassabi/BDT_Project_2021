# necessary to import other modules
import sys
sys.path.append('../')

from functions.mysql import *
from functions.utilities import *
import time


"""
# This code is meant to be executed once
# It creates a clean .csv with all the AGGIUDICATARI data

Input:
    > agg_path: directory in which we find all the AGGIUDICATARI .csv
    > save_path: directory in which we store the final .csv with the cleaned and merged data
    > final_csv_name: name of the final .csv output
"""
def cleanAggiudicatari(agg_path, save_path, final_csv_name):
    # Import, clean and merge all AGGIUDICATARI data
    print("\n> Importing all AGGIUDICATARI datasets")
    all_agg_df = mergeAggiudicatari(agg_path)
    print("> All AGGIUDICATARI cleaned and saved into a dataframe")

    # Print some info on the clean data
    print("\n> Dataset sample and information\n")
    print(all_agg_df.head())
    print("\nTotal number of rows:", all_agg_df.shape[0])

    # Save the dataset as .csv
    print("\n> Saving the dataset...")
    all_agg_df.to_csv(save_path + final_csv_name, index = False, sep=";")
    print("> Dataset correctly saved. Directory:", save_path)


"""
# This code is meant to be executed once
# It exports the clean .csv with all the AGGIUDICATARI data to a MySQL DB
"""
def exportAggiudicatariToMySQL(agg_path, host, port, database, user, password):

    agg_table_name = "elenco_aggiudicatari_test"
    agg_cols_list = ["cig", "aggiudicatario", "tipo_aggiudicatario"]

    # Final AGGIUDICATARI .csv data import
    print("\n> Importing the data from the AGGIUDICATARI .csv")
    df = importAggiudicatari(agg_path)

    # Establish MySQL connection
    connection = connectToMySQL(host, port, database, user, password, False)
    setAutocommit(connection, True)
    cursor = createCursor(connection)

    # Execute the query
    print("\n> Inserting data into", agg_table_name)
    insertDataInTable(df, cursor, agg_table_name, agg_cols_list)
    print("> BD correctly updated")

    # Close the connection
    closeMySQLConnection(cursor, connection)


"""
# This code is meant to be executed once

# 1. It imports, cleans and merges all the CIG data
# 2. It imports the already cleaned AGGIUDICATARI data
# 3. It merges the data based on "cig"
# 4. It stores the data as .csv
"""
def cleanCIG(cig_path, agg_path, save_path, final_csv_name):
    
    # Import, clean and merge all CIG data
    print("\n> Importing all CIG datasets")
    all_cig_df = mergeCIG(cig_path)
    print("> All CIGs cleaned and saved into a dataframe")

    # Import clean and already merged AGGIUDICATARI data
    print("\n> Importing AGGIUDICATARI dataset")
    all_agg_df = importAggiudicatari(agg_path)

    # Join the data
    print("\n> Joining the CIG and the AGGIUDICATARI dataset")
    full_df = joinCIGAggiudicatari(all_cig_df, all_agg_df)
    print("> Join performed correctly")

    # Print some info on the data
    print("\n> Dataset sample and information\n")
    print(full_df.head())
    print("\nTotal number of rows:", full_df.shape[0])

    # Save the dataset as .csv
    print("\n> Saving the dataset...")
    full_df.to_csv(save_path + final_csv_name, index = False, sep=";")
    print("> Dataset correctly saved in '", save_path, "'")


"""
# This code is meant to be executed once
# It exports the clean .csv with all the CIG join AGGIUDICATARI data to a MySQL DB
"""
def exportCIGAggiudicatariToMySQL(agg_cig_csv_path, host, port, database, user, password):

    agg_cig_table_name = "appalti_aggiudicatari_test"
    agg_cig_cols_list = ["cig", "numero_gara", "importo_complessivo_gara", "n_lotti_componenti", "importo_lotto", "settore", "data_pubblicazione", "tipo_scelta_contraente", "modalita_realizzazione", "denominazione_amministrazione_appaltante", "sezione_regionale", "descrizione_cpv", "aggiudicatario", "tipo_aggiudicatario"]

    # Dataset import
    print("\n> Importing the data from the CIG_AGGIUDICATARI .csv")
    df = pd.read_csv(agg_cig_csv_path, sep=";")

    # Establish MySQL connection
    connection = connectToMySQL(host, port, database, user, password, False)
    setAutocommit(connection, True)
    cursor = createCursor(connection)

    # Execute the query
    insertDataInTable(df, cursor, agg_cig_table_name, agg_cig_cols_list)

    # Close the connection
    closeMySQLConnection(cursor, connection)
# necessary to import other modules
import sys
sys.path.append('../')

from functions.mysql import *
from functions.utilities import *

"""
FUNCTIONS FOR UPDATE OF MYSQL DATABASE
"""

"""
Updates the AGGIUDICATARI table in a MySQL DB

Input:
    > host
    > port
    > database
    > user
    > password
    > agg_csv_path: path of (raw) AGGIUDICATARI .csv with updated data
"""
def updateAggiudicatariTable(host, port, database, user, password, agg_csv_path, interface = False):
    
    # Query information
    agg_table_name = "elenco_aggiudicatari_test"
    cols_list = ["cig", "aggiudicatario", "tipo_aggiudicatario"]

    print("\n> Updating AGGIUDICATARI datasets")

    if interface:
        refreshGUI()

    new_agg_df = importAggiudicatari(agg_csv_path)
    print("> AGGIUDICATARI .csv correctly imported")

    if interface:
        refreshGUI()

    # Clean the AGGIUDICATARI df
    new_agg_df = cleanAggiudicatari(new_agg_df)
    print("> AGGIUDICATARI data cleaned")

    if interface:
        refreshGUI()

    # Establish MySQL connection (alchemy)
    db_connection = connectToMySQL_Alchemy(host, port, database, user, password, False)

    if interface:
        refreshGUI()

    # Retrieve the current AGGIUDICATARI data
    old_agg_df = retrieveAllDataFromTable_Alchemy(agg_table_name, db_connection)

    if interface:
        refreshGUI()

    # Find only new data
    new_entries = pd.concat([old_agg_df,new_agg_df]).drop_duplicates(keep=False)

    if interface:
        refreshGUI()

    # Establish MySQL connection
    connection = connectToMySQL(host, port, database, user, password, False)
    setAutocommit(connection, True)
    cursor = createCursor(connection)

    if interface:
        refreshGUI()

    # Inserting new AGGIUDICATARI data into the db
    print("\n> Inserting new data into", agg_table_name)
    insertDataInTable(new_entries, cursor, agg_table_name, cols_list, interface)
    print("\n> BD correctly updated")

    if interface:
        refreshGUI()


"""
Updates the AGGIUDICATARI table in a MySQL DB

Input:
    > host
    > port
    > database
    > user
    > password
    > agg_csv_path: path of (raw) AGGIUDICATARI .csv with updated data
"""
def updateAggiudicatariTable_slow(host, port, database, user, password, agg_csv_path, interface = False):

    # Query information
    agg_table_name = "elenco_aggiudicatari_test"
    agg_cols_list = ["cig", "aggiudicatario", "tipo_aggiudicatario"]

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
    query = "TRUNCATE `" + database + "`.`" + agg_table_name + "`;"
    cursor.execute(query)
    print("\n> Table " + agg_table_name + " correctly truncated on MySQL DB")

    # Inserting new AGGIUDICATARI data into the db
    print("> Inserting new data into", agg_table_name)
    insertDataInTable(agg_df, cursor, agg_table_name, agg_cols_list, interface)
    print("> BD correctly updated")

    # Close MySQL connection
    closeMySQLConnection(cursor, connection)


"""
Updates the CIG join AGGIUDICATARI table in a MySQL DB

Input:
    > host
    > port
    > database
    > user
    > password
    > cig_csv_path: path of (raw) CIG .csv with updated data
"""
def updateCIGTable(host, port, database, user, password, cig_csv_path, interface = False):

    # Query information
    agg_table_name = "elenco_aggiudicatari"
    agg_cig_table_name = "appalti_aggiudicatari_test"
    agg_cig_cols_list = ["cig", "numero_gara", "importo_complessivo_gara", "n_lotti_componenti", "importo_lotto", "settore", "data_pubblicazione", "tipo_scelta_contraente", "modalita_realizzazione", "denominazione_amministrazione_appaltante", "sezione_regionale", "descrizione_cpv", "aggiudicatario", "tipo_aggiudicatario"]

    print("\n> Updating CIG AGGIUDICATARI datasets")

    if interface:
        refreshGUI()

    # Prompt the user to select a .csv
    cig_df = importCIG(cig_csv_path)
    print("> CIG .csv correctly imported")

    if interface:
        refreshGUI()

    # Clean the CIG df
    cig_df = cleanCIG(cig_df)
    print("> CIG data cleaned")

    if interface:
        refreshGUI()

    # Retrieval of AGGIUDICATARI from MySQL DB
    print("\n> Retrieving AGGIUDICATARI data from MySQL DB")

    # 1. Establish MySQL connection
    db_connection = connectToMySQL_Alchemy(host, port, database, user, password, False)

    if interface:
        refreshGUI()

    # 2. Retrieve the AGGIUDICATARI data
    agg_df = retrieveAllDataFromTable_Alchemy(agg_table_name, db_connection)

    print("> AGGIUDICATARI data retrieved")

    if interface:
        refreshGUI()

    # Inner Join of new CIG data and AGGIUDICATARI
    print("\n> Joining CIG data with AGGIUDICATARI data")
    full_df = joinCIGAggiudicatari(cig_df, agg_df)

    if interface:
        refreshGUI()

    # Add new data to MySQL appalti_aggiudicatari table

    # A. connect to db
    connection = connectToMySQL(host, port, database, user, password, False)
    setAutocommit(connection, True)
    cursor = createCursor(connection)

    if interface:
        refreshGUI()

    # B. execute the query
    print("\n> Inserting data into", agg_cig_table_name)
    insertDataInTable(full_df, cursor, agg_cig_table_name, agg_cig_cols_list, interface)
    print("\n> BD correctly updated")

    # C. close the connection
    closeMySQLConnection(cursor, connection)

    if interface:
        refreshGUI()

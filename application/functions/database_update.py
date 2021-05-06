from functions.mysql import *

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
def updateAggiudicatariTable(host, port, database, user, password, agg_csv_path):
    
    # Query information
    table_name = "elenco_aggiudicatari_test"
    cols_list = ["cig", "aggiudicatario", "tipo_aggiudicatario"]

    # Tracking the time
    start = time.time()

    print("\n> Updating AGGIUDICATARI datasets")

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
    print("\n> BD correctly updated")

    # Calculate and print total time
    end = time.time()
    print("\n> Elapsed time:", from_seconds_to_elapsed_time(end - start))


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
def updateCIGTable(host, port, database, user, password, cig_csv_path):
    table_agg = "elenco_aggiudicatari"
    table_cig_agg = "appalti_aggiudicatari_test"
    cols_list = ["cig", "numero_gara", "importo_complessivo_gara", "n_lotti_componenti", "importo_lotto", "settore", "data_pubblicazione", "tipo_scelta_contraente", "modalita_realizzazione", "denominazione_amministrazione_appaltante", "sezione_regionale", "descrizione_cpv", "aggiudicatario", "tipo_aggiudicatario"]


    # Tracking the time
    start = time.time()

    print("\n> Updating CIG AGGIUDICATARI datasets")

    # Prompt the user to select a .csv
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
    print("\n> BD correctly updated")

    # C. close the connection
    closeMySQLConnection(cursor, connection)

    # Calculate and print total time
    end = time.time()
    print("\n> Elapsed time:", from_seconds_to_elapsed_time(end - start))
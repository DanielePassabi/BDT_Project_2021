# IMPORT LIBRARIES
import pandas as pd
from sklearn import neighbors
import numpy as np

import sys
import time

from os import listdir
from os.path import isfile, join
from tqdm import tqdm

import mysql.connector
from sqlalchemy import create_engine

"""
FUNCTIONS FOR NEW DATAFRAMES
"""

"""
Get all the CIG datasets in a specified directory, clean them and merge them. 

Input: directory's path of CIG datasets
Output: unique, cleaned CIG dataframe (pandas) 
"""
def mergeCIG(cigs_path):

    # get the list of file names to import
    file_names = [f for f in listdir(cigs_path) if isfile(join(cigs_path, f))]

    # dataframes list placeholder
    frames = []

    # iterate over every CIG dataset
    for file_name in tqdm(file_names, desc="> Cleaning and merging CIGs"):

        # get the path
        temp_cig_path = cigs_path + file_name
        
        # import the CIG df
        temp_cig_df = importCIG(temp_cig_path)

        # clean the CIG df
        temp_cleaned_cig_df = cleanCIG(temp_cig_df)

        # add it to the dataframes list
        frames.append(temp_cleaned_cig_df)
    
    # return the complete and cleaned dataset
    final_df = pd.concat(frames)
    return final_df


"""
Import a CIG dataset

Input: path of CIG dataset
Output: CIG dataframe (pandas)
"""
def importCIG(cig_path):
    df = pd.read_csv(cig_path, sep=";", low_memory=False)
    return df


"""
Cleans a CIG dataframe 

Input: CIG dataframe (pandas)
Output: clean CIG dataframe
    > only meaningful columns kept
    > all rows with at least 1 missing value removed
"""
def cleanCIG(cig_df):

    # Operation 1 - Select only meaningful columns
    meaningful_cols = ["cig", "numero_gara","importo_complessivo_gara", "n_lotti_componenti", "importo_lotto", "settore", "data_pubblicazione", "tipo_scelta_contraente", "modalita_realizzazione", "denominazione_amministrazione_appaltante", "sezione_regionale", "descrizione_cpv"]
    cig_df = cig_df[meaningful_cols]

    # Operation 2 - Remove all rows with at least 1 NAs
    cig_df = cig_df.dropna()

    # Return clean df
    return cig_df


"""
Get all the Aggiudicatari datasets in a specified directory, clean them and merge them. 

Input: directory's path of Aggiudicatari datasets
Output: unique, cleaned Aggiudicatari dataframe (pandas) 
"""
def mergeAggiudicatari(aggiudicatari_path):

    # get the list of file names to import
    file_names = [f for f in listdir(aggiudicatari_path) if isfile(join(aggiudicatari_path, f))]

    # create placeholder dataset
    final_df = pd.DataFrame()

    # iterate over every Aggiudicatari dataset
    for file_name in tqdm(file_names, desc="> Cleaning and merging Aggiudicatari"):

        # get the path
        temp_agg_path = aggiudicatari_path + file_name
        
        # import the Aggiudicatari df
        temp_agg_df = importAggiudicatari(temp_agg_path)

        # clean the Aggiudicatari df
        temp_cleaned_agg_df = cleanAggiudicatari(temp_agg_df)

        # add it to the final df
        frames = [final_df, temp_cleaned_agg_df]
        final_df = pd.concat(frames)

    # return the complete and cleaned dataset
    return final_df


"""
Import an Aggiudicatori dataset

Input: path of Aggiudicatori dataset
Output: Aggiudicatori dataframe (pandas)
"""
def importAggiudicatari(agg_path):
    df = pd.read_csv(agg_path, sep=";", low_memory=False)
    return df


"""
Cleans a Aggiudicatori dataframe 

Input: Aggiudicatori dataframe (pandas)
Output: clean Aggiudicatori dataframe
    > only meaningful columns kept
    > renaming of columns for clarity
    > all rows with at least 1 missing value removed
"""
def cleanAggiudicatari(agg_df):
    # Operation 1 - Select only meaningful columns
    meaningful_cols = ["cig", "denominazione", "tipo_soggetto"]
    agg_df = agg_df[meaningful_cols]

    # Operation 2 - Renaming of columns (for clarity)
    agg_df = agg_df.rename(columns={"denominazione": "aggiudicatario", "tipo_soggetto": "tipo_aggiudicatario"})

    # Operation 3 - Remove all rows with at least 1 NAs
    agg_df = agg_df.dropna()

    # Return clean df
    return agg_df


"""
Perform the join on the CIG dataframe and the Aggiudicatari dataframe
    > inner join
    > on *cig*

Input:
    > CIG dataframe
    > Aggiudicatari dataframe
Output: joined dataframe
"""
def joinCIGAggiudicatari(cig_df, agg_df):

    # join the datasets on cig (inner join)
    full_df = pd.merge(cig_df, agg_df, on='cig', how='inner')
    #full_df = pd.merge(cig_df, agg_df, on='cig', how='left')

    # return the complete dataframe
    return full_df


"""
FUNCTIONS FOR MYSQL
"""

"""
Establish a MySQL Connection (using the package sqlalchemy)

Input:
    > host
    > port
    > database
    > user
    > password
    > showInfo: boolean value
Output: connection object
"""
def connectToMySQL_Alchemy(host, port, database, user, password, showInfo):
    if showInfo:
        print("\n> Trying to connect to MySQL Server with the following parameters")
        print("   - host:", host)
        print("   - port:", port)
        print("   - database:", database)
        print("   - user:", user)

    try:
        connection_str = "mysql+pymysql://" + user + ":" + password + "@" + host + "/" + database
        connection = create_engine(connection_str)

        if showInfo:
            print("\n> Successfully connected")
        return connection

    except Exception as e:
        print("\n> ERROR: cannot connect to the database. Error details below.\n" + str(e))
        sys.exit("\n> Execution Interrupted")


"""
Retrieve all data from specified table

Input:
    > table
    > connection (sqlalchemy object)
Output:
    > table (in pandas dataframe form)
"""
def retrieveAllDataFromTable_Alchemy(table, connection):
    query = "SELECT * FROM " + table
    res_df = pd.read_sql(query, con=connection)
    return res_df


"""
Establish a MySQL Connection

Input:
    > host
    > port
    > database
    > user
    > password
    > showInfo: boolean value
Output: connection object
"""
def connectToMySQL(host, port, database, user, password, showInfo):
    if showInfo:
        print("\n> Trying to connect to MySQL Server with the following parameters")
        print("   - host:", host)
        print("   - port:", port)
        print("   - database:", database)
        print("   - user:", user)

    try:
        connection = mysql.connector.connect(
            host = host,
            port = port,
            database = database,
            user = user,
            password = password
        )

        if showInfo:
            print("\n> Successfully connected")
        return connection

    except Exception as e:
        print("\n> ERROR: cannot connect to the database. Error details below.\n" + str(e))
        sys.exit("\n> Execution Interrupted")


"""
Set the autocommit to either True or False

Input:
    > connection object
    > boolean value
Output: none
"""
def setAutocommit(connection, bool_value):
    connection.autocommit = bool_value
    #print("> Autocommit set to", bool_value)


"""
Create a cursor

Input: connection object
Output: cursor
"""
def createCursor(connection):
    return connection.cursor()


"""
Insert into the connected MySQL db the data from the given dataframe

Input:
    > df: dataframe with the data to add to the db
    > cursor
    > table_name: name of the table in which the information will be added
    > cols_list: list of columns present in both the df and the table
"""
def insertDataInTable(df, cursor, table_name, cols_list):

    # Get the names of all the columns (in string format for MySQL)
    cols_names = "("
    for col in cols_list:
        cols_names = cols_names + col + ","
    cols_names = cols_names[:-1] + ")"

    # Get all the placeholders set
    values_placeholders = "("
    for i in range(len(cols_list)):
        values_placeholders = values_placeholders + "%s,"
    values_placeholders = values_placeholders[:-1] + ")"

    # create the query
    query = "INSERT into " + table_name + " " + cols_names + " VALUES " + values_placeholders

    # execute the query
    #print("\n> Inserting data into", table_name, "table")

    # tqdm does not work --> we track % manually
    total_rows = df.shape[0]

    try:

        for i, row in df.reset_index().iterrows():

            completion_perc = str(round(((i+1) / total_rows) * 100, 2))
            print("\r> Inserting rows: " + str(i+1) + "/" + str(total_rows) + " [" + completion_perc + "%]", end="")

            query_list = []
            for col in cols_list:
                query_list.append(row[col])

            cursor.execute(query, tuple(query_list))
        
    except Exception as e:
        print("\n> ERROR: cannot add the row to the database. Error details below.\n" + str(e))
        sys.exit("\n> Execution Interrupted")


"""
Closes the connection with MySQL server

Input:
    > cursor
    > connection
Output: none
"""
def closeMySQLConnection(cursor, connection):
    cursor.close()
    connection.close()
    #print("> MySQL connection closed successfully")


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



"""
FUNCTIONS FOR MACHINE LEARNING MODEL
"""

"""
Train a KNN model

Input:
    > dataframe, which *must* have the following columns:
        * importo_complessivo_gara
        * n_lotti_componenti
        * importo_lotto
        * aggiudicatario
    > number of neighbours (K for KNN)
Output: KNN model
"""
def train_KNN_model(df, K):

    # get the data about *lotti*
    lotti_data = []
    for i in range(len(df)):
        lotti_data.append([df["importo_complessivo_gara"][i], df["n_lotti_componenti"][i], df["importo_lotto"][i]])

    # get the data about *aggiudicatari*
    lotti_target = df["aggiudicatario"]

    # train the knn model
    X, y = lotti_data, lotti_target
    knn = neighbors.KNeighborsClassifier(n_neighbors=K)
    knn.fit(X, y)

    return knn


"""
Get a new prediction of the trained KNN model

Input:
    > KNN model
    > importo_complessivo_gara
    > n_lotti_componenti
    > importo_lotto
Output: prediction
"""
def get_new_KNN_pred(KNN_model, importo_complessivo_gara, n_lotti_componenti, importo_lotto):
    return knn.predict([[importo_complessivo_gara, n_lotti_componenti, importo_lotto]])


"""
UTILITY FUNCTIONS
"""

"""
Convert seconds in hours, minutes, seconds
"""
def from_seconds_to_elapsed_time(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
      
    return "%d:%02d:%02d" % (hour, minutes, seconds)
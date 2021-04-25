# IMPORT LIBRARIES
import pandas as pd
from sklearn import neighbors
import numpy as np

import sys

from os import listdir
from os.path import isfile, join
from tqdm import tqdm

import mysql.connector

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
    for file_name in tqdm(file_names, desc=">> Cleaning and merging CIGs"):

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
    for file_name in tqdm(file_names, desc=">> Cleaning and merging Aggiudicatari"):

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
Establish a MySQL Connection

Input:
    > host
    > port
    > database
    > user
    > password
Output: connection object
"""
def connectToMySQL(host, port, database, user, password):
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
            password = "dany1998"
        )

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
    print("> Autocommit set to", bool_value)


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
def executeInsertQuery(df, cursor, table_name, cols_list):

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
    print("\n> DB population started")

    # tqdm does not work --> we track % manually
    total_rows = df.shape[0]
    n = 1

    try:

        for i, row in df.iterrows():
            
            if (i % 50000 == 0 and i != 0):
                rows_updated = n*i
                completion_perc = round(rows_updated / total_rows, 4)
                print(">> Completed: ", completion_perc, "%")
                n = n+1

            query_list = []
            for col in cols_list:
                query_list.append(row[col])

            cursor.execute(query, tuple(query_list))
        
    except Exception as e:
        print("\n> ERROR: cannot add the row to the database. Error details below.\n" + str(e))
        sys.exit("\n> Execution Interrupted")
        

    print("\n> Data added to the database")


"""
Closes the connection with MySQL server

Input:
    > cursor
    > connection
Output: none
"""
def closeMySQLConnection(cursor, connection):
    print("\n> Closing the connection")
    cursor.close()
    connection.close()
    print("> Connection closed successfully")


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
      
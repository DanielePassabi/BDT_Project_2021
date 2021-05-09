# necessary to import other modules
import sys
sys.path.append('../')

import pandas as pd
import numpy as np

import mysql.connector
from sqlalchemy import create_engine
import wx

from functions.utilities import *

"""
FUNCTIONS FOR MYSQL [sqlalchemy]
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
FUNCTIONS FOR MYSQL [mysql.connector]
"""

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
def insertDataInTable(df, cursor, table_name, cols_list, interface = False):

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

        already_displayed = []
        for i, row in df.reset_index().iterrows():

            if interface:
                completion_perc = int( ((i+1) / total_rows) * 100)
                if completion_perc % 5 == 0 and completion_perc not in already_displayed:
                    print("   - Completion: " + str(completion_perc) + "%")
                    already_displayed.append(completion_perc)
            else:
                completion_perc = str(round(((i+1) / total_rows) * 100, 2))
                print("\r> Inserting rows: " + str(i+1) + "/" + str(total_rows) + " [" + completion_perc + "%]", end="")

            query_list = []
            for col in cols_list:
                query_list.append(row[col])

            cursor.execute(query, tuple(query_list))

            # send the information to the console (prevent freezing)
            if interface:
                refreshGUI()

        
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


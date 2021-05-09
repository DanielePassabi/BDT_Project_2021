# IMPORT LIBRARIES
import pandas as pd
import numpy as np
from sklearn import neighbors

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
    lotti_target = list(df["aggiudicatario"])

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
    return KNN_model.predict([[importo_complessivo_gara, n_lotti_componenti, importo_lotto]])


"""

"""
def prepareInputForKNN(df):
    lotti_data = []
    for i in range(len(test_df)):
        lotti_data.append([test_df["importo_complessivo_gara"][i], test_df["n_lotti_componenti"][i], test_df["importo_lotto"][i]])

    # get the data about *aggiudicatari*
    lotti_target = list(test_df["aggiudicatario"])

    return [lotti_data,lotti_target]
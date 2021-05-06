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

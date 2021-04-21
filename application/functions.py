# IMPORT LIBRERIE
import pandas as pd
from sklearn import neighbors
import numpy as np

"""
Funzione per addestrare un modello KNN, a partire da:
    > dataset, che deve avere le colonne
        * importo_complessivo_gara
        * n_lotti_componenti
        * importo_lotto
        * aggiudicatore
    > numero di neighbours (K per KNN)
"""
def train_KNN_model(df, K):

    # Ottengo i dati sui lotti
    lotti_data = []
    for i in range(len(df)):
        lotti_data.append([df["importo_complessivo_gara"][i], df["n_lotti_componenti"][i], df["importo_lotto"][i]])

    # Ottengo i dati sugli aggiudicatori
    lotti_target = df["aggiudicatore"]

    # Addestro il modello
    X, y = lotti_data, lotti_target
    knn = neighbors.KNeighborsClassifier(n_neighbors=K)
    return knn.fit(X, y)


"""
Funzione per ottenere una nuova predizione, a partire da:
    > importo_complessivo_gara
    > n_lotti_componenti
    > importo_lotto
"""
def get_new_KNN_pred(importo_complessivo_gara, n_lotti_componenti, importo_lotto):
    return knn.predict([[importo_complessivo_gara, n_lotti_componenti, importo_lotto]])
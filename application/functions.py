# IMPORT LIBRERIE
import pandas as pd
from sklearn import neighbors
import numpy as np

#
# FUNZIONI PER IMPORT DATAFRAME
#

def unisciCIG(cigs_path):

    # conta file nella cartella

    # ottiene i nomi dei file

    # ottiene i file usando importaCIG

    # usa la funzione pulisciCIG su ogni df

    # unisce in un dataset unico di CIG

    pass

"""
Importa un dataset CIG
Input: path del dataset CIG
Output: pandas dataframe
"""
def importaCIG(cig_path):
    df = pd.read_csv(cig_path, sep=";")
    return df

def pulisciCIG(cig_df):

    # vedi operazioni di KNIME e replica
    pass


def importaAggiudicatori(agg_path):

    # importa il dataframe 
    pass

def pulisciAggiudicatori(agg_df):

    # vedi operazioni di KNIME e replica
    pass


def joinCIGAggiudicatori(cig_df, agg_df):
    pass



#
# FUNZIONI PER ARCHITETTURA
#

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
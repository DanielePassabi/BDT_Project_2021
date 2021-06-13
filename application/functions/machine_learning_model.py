# IMPORT LIBRARIES

import pickle

from sklearn.preprocessing import OneHotEncoder
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier

"""
FUNCTIONS FOR MACHINE LEARNING MODEL
"""



"""
# █▄▀ ▄▄ █▄░█ █▀▀ █ █▀▀ █░█ █▄▄ █▀█ █▀█ █▀   █▀▀ █░░ ▄▀█ █▀ █▀ █ █▀▀ █ █▀▀ █▀█
# █░█ ░░ █░▀█ ██▄ █ █▄█ █▀█ █▄█ █▄█ █▀▄ ▄█   █▄▄ █▄▄ █▀█ ▄█ ▄█ █ █▀░ █ ██▄ █▀▄
"""

"""
Function that:
    > will create and save a OneHotEncoder (to cope with categorical variables)
    > will create, train and save a KNN Classifier

Input:
    > training_data
    > K: parameter for KNN
"""
def create_KNeighborsClassifier(training_data, K, save_dir):
    
    # get the label
    Y_label = training_data['aggiudicatario'].tolist()

    # remove the columns that do not provide information from the data
    X = training_data.drop(['cig', 'numero_gara', 'data_pubblicazione', 'aggiudicatario'], axis=1)

    # create the encoder 
    # handle_unknown='ignore' --> used to deal with new possible parameters
    knn_encoder = OneHotEncoder(handle_unknown='ignore').fit(X)

    # save the encoder (we need it for future predictions)
    filename = save_dir + "/KNeighborsClassifier_encoder.sav"
    pickle.dump(knn_encoder, open(filename, 'wb'))

    # encode the training data
    X_encoded = knn_encoder.transform(X)

    # create the model
    knn_classifier = KNeighborsClassifier(K)
    knn_classifier.fit(X_encoded, Y_label)

    # save the model to disk
    filename = save_dir + "/KNeighborsClassifier_model.sav"
    pickle.dump(knn_classifier, open(filename, 'wb'))

    print("> Model created, related information saved on disk.")

    # return the model (and the encoder)
    return knn_classifier, knn_encoder


"""
Function to obtain the n nearest neighbours

Problem: it return indexes and distances
         we need the training set to get the data --> too expensive
"""
def get_n_pred_KNeighborsClassifier(model, encoder, input_data, n):

    # encode the input data
    encoded_input = encoder.transform([input_data])

    distances, indices = model.kneighbors(encoded_input,  n_neighbors=n)
    return distances, indices



"""
█▀█ ▄▀█ █▄░█ █▀▄ █▀█ █▀▄▀█   █▀▀ █▀█ █▀█ █▀▀ █▀ ▀█▀   █▀▀ █░░ ▄▀█ █▀ █▀ █ █▀▀ █ █▀▀ █▀█
█▀▄ █▀█ █░▀█ █▄▀ █▄█ █░▀░█   █▀░ █▄█ █▀▄ ██▄ ▄█ ░█░   █▄▄ █▄▄ █▀█ ▄█ ▄█ █ █▀░ █ ██▄ █▀▄
"""

"""
Function that:
    > will create and save a OneHotEncoder (to cope with categorical variables)
    > will create, train and save a Random Forest Classifier

Input:
    > training_data

Problem: too memory demanding
"""
def create_RandomForestClassifier(training_data):
    
    # get the label
    Y_label = training_data['aggiudicatario'].tolist()

    # remove the columns that do not provide information from the data
    X = training_data.drop(['cig', 'numero_gara', 'data_pubblicazione', 'aggiudicatario', 'denominazione_amministrazione_appaltante'], axis=1)

    # create the encoder 
    # handle_unknown='ignore' --> used to deal with new possible parameters
    rf_encoder = OneHotEncoder(handle_unknown='ignore').fit(X)

    # save the encoder (we need it for future predictions)
    filename = "models_data/RandomForestClassifier_encoder.sav"
    pickle.dump(rf_encoder, open(filename, 'wb'))

    # encode the training data
    X_encoded = rf_encoder.transform(X)

    ### sopra va incluso in una funzione perchè il codice è uguale :|

    # create the model
    rf_classifier = RandomForestClassifier()
    rf_classifier.fit(X_encoded, Y_label)

    # save the model to disk
    filename = "models_data/RandomForestClassifier_model.sav"
    pickle.dump(rf_classifier, open(filename, 'wb'))

    print("> Model created, related information saved on disk.")

    # return the model (and the encoder)
    return rf_classifier, rf_encoder



"""
█▀▄▀█ █░░ █▀█   █▀▀ █░░ ▄▀█ █▀ █▀ █ █▀▀ █ █▀▀ █▀█
█░▀░█ █▄▄ █▀▀   █▄▄ █▄▄ █▀█ ▄█ ▄█ █ █▀░ █ ██▄ █▀▄
"""

"""
Function that:
    > will create and save a OneHotEncoder (to cope with categorical variables)
    > will create, train and save a MLPClassifier

Input:
    > training_data

Problem: too memory demanding
"""
def create_MLPClassifier(training_data):
    
    # get the label
    Y_label = training_data['aggiudicatario'].tolist()

    # remove the columns that do not provide information from the data
    X = training_data.drop(['cig', 'numero_gara', 'data_pubblicazione', 'aggiudicatario', 'denominazione_amministrazione_appaltante'], axis=1)

    # create the encoder 
    # handle_unknown='ignore' --> used to deal with new possible parameters
    snn_encoder = OneHotEncoder(handle_unknown='ignore').fit(X)

    # save the encoder (we need it for future predictions)
    filename = "models_data/MLPClassifier_encoder.sav"
    pickle.dump(snn_encoder, open(filename, 'wb'))

    # encode the training data
    X_encoded = snn_encoder.transform(X)

    ### sopra va incluso in una funzione perchè il codice è uguale :|

    # create the model
    snn_classifier = MLPClassifier()
    snn_classifier.fit(X_encoded, Y_label)

    # save the model to disk
    filename = "models_data/MLPClassifier_model.sav"
    pickle.dump(snn_classifier, open(filename, 'wb'))

    print("> Model created, related information saved on disk.")

    # return the model (and the encoder)
    return snn_classifier, snn_encoder



"""
▄▀█ █░░ █░░   █▀▄▀█ █▀█ █▀▄ █▀▀ █░░ █▀
█▀█ █▄▄ █▄▄   █░▀░█ █▄█ █▄▀ ██▄ █▄▄ ▄█
"""

"""
Function to test the performances of a sklearn classifier

Input:
    > model: a sklearn classifier
    > encoder: the OneHotEncoder used to preprocess the data for the model
    > test_data
"""
def test_model(model, encoder, test_data):

    # get the label
    Y_label = test_data['aggiudicatario'].tolist()

    # remove the columns that do not provide information from the data
    X = test_data.drop(['cig', 'numero_gara', 'data_pubblicazione', 'aggiudicatario'], axis=1)

    # encode the test data
    X_encoded = encoder.transform(X)

    # test the model --> compute R^2
    acc = model.score(X_encoded, Y_label, sample_weight=None)

    # return the result
    return acc

"""
Function to get a new prediction, given input data

Input:
    > model: a sklearn classifier
    > encoder: the OneHotEncoder used to preprocess the data for the model
    > input_data: list with
       - importo_complessivo_gara
       - n_lotti_componenti
       - importo_lotto
       - settore
       - tipo_scelta_contraente
       - modalita_realizzazione
       - denominazione_amministrazione_appaltante
       - sezione_regionale
       - descrizione_cpv
       - tipo_aggiudicatari
"""
def get_pred(model, encoder, input_data):

    # encode the input data
    encoded_input = encoder.transform([input_data])

    # get the prediction and return it
    return model.predict(encoded_input)[0]





"""
█░█ ▀█▀ █ █░░ █ ▀█▀ █▄█   █▀▀ █░█ █▄░█ █▀▀ ▀█▀ █ █▀█ █▄░█ █▀
█▄█ ░█░ █ █▄▄ █ ░█░ ░█░   █▀░ █▄█ █░▀█ █▄▄ ░█░ █ █▄█ █░▀█ ▄█
"""

def one_hot_encode_data(df):
    pass












# necessary to import other modules
import sys
sys.path.append('../')

from functions.machine_learning_model import *
from config import *

import pickle

################
### SETTINGS ###
################

# Input for prediction
importo_complessivo_gara = input_for_prediction["importo_complessivo_gara"]
n_lotti_componenti = input_for_prediction["n_lotti_componenti"]
importo_lotto = input_for_prediction["importo_lotto"]
settore = input_for_prediction["settore"]
tipo_scelta_contraente = input_for_prediction["tipo_scelta_contraente"]
modalita_realizzazione = input_for_prediction["modalita_realizzazione"]
denominazione_amministrazione_appaltante = input_for_prediction["denominazione_amministrazione_appaltante"]
sezione_regionale = input_for_prediction["sezione_regionale"]
descrizione_cpv = input_for_prediction["descrizione_cpv"]
tipo_aggiudicatari = input_for_prediction["tipo_aggiudicatari"]

# Model info
model_path = model_info["model_path"]
encod_path = model_info["encod_path"]


##############
### SCRIPT ###
##############

# Load model and encoder
KNeighborsClassifier_model = pickle.load(open(model_path, 'rb'))
KNeighborsClassifier_encoder = pickle.load(open(encod_path, 'rb'))

# Prepare list with input data
input_data = [importo_complessivo_gara, n_lotti_componenti, importo_lotto, settore, tipo_scelta_contraente, modalita_realizzazione, denominazione_amministrazione_appaltante, sezione_regionale, descrizione_cpv, tipo_aggiudicatari]

# Return prediction
pred = get_pred(KNeighborsClassifier_model, KNeighborsClassifier_encoder, input_data)
print("> Prediction:", pred)






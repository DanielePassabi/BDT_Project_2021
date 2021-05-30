# necessary to import other modules
import sys
sys.path.append('../../')

from functions.utilities import *

import pandas as pd
import json

print("> Importing the data")
# Import data from MySQL
df = pd.read_csv("../../../application/datasets/clean_data/appalti_aggiudicatari.csv", sep=";")

print("> Creating the dictionary with all possible inputs")
# Create the dict
cols_list = ["settore", "tipo_scelta_contraente", "modalita_realizzazione", "denominazione_amministrazione_appaltante", "sezione_regionale", "descrizione_cpv", "tipo_aggiudicatario"]
choices_dict = createDictPossibleChoicesForPrediction(df, cols_list)

# Save the dict
with open('../config/input_possible_choices.json', 'w') as json_file:
    json.dump(choices_dict, json_file)

print("> .json correctly stored")
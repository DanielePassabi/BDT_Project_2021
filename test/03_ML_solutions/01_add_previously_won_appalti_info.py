import pandas as pd
from tqdm import tqdm

# Import the data
df = pd.read_csv("../../application/datasets/clean_data/appalti_aggiudicatari.csv", sep=";")

print("\nTotal rows:", df.shape[0])
print("Total cols:", df.shape[1])


# Add information
# riguardo aste con stessa denominazione appaltante vinte precedentemente da un aggiudicatario
vincita_precedente_con_amm_app = []
agg_amm_app_couples = []

for index, row in tqdm(df.iterrows()):
    temp_couple = [row['aggiudicatario'], row['denominazione_amministrazione_appaltante']]
    if temp_couple in agg_amm_app_couples:
        vincita_precedente_con_amm_app.append(1)
    else:
        vincita_precedente_con_amm_app.append(0)
    agg_amm_app_couples.append(temp_couple)

# Print some info
print("Total 0:", vincita_precedente_con_amm_app.count(0))
print("Total 1:", vincita_precedente_con_amm_app.count(1))

# Add the data to the dataframe
df["vincita_precedente_con_amm_app"] = vincita_precedente_con_amm_app

# Save the dataset
df.to_csv("appalti_aggiudicatari_custom.csv", sep=";")

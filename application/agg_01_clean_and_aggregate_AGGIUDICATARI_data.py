from functions import *
import time

start = time.time()

print("\n> Importing all AGGIUDICATARI datasets")
aggs_path = "datasets/aggiudicatari/"
all_aggs_df = mergeAggiudicatari(aggs_path)
print("> All AGGIUDICATARI cleaned and saved into a dataframe")

print("\n> Dataset sample and information\n")
print(all_aggs_df.head())

print("\nTotal number of rows:", all_aggs_df.shape[0])

print("\n> Saving the dataset...")

save_path = "datasets/clean_data/"
dataset_name = "aggiudicatari.csv"

all_aggs_df.to_csv(save_path + dataset_name, index = False, sep=";")

print("> Dataset correctly saved in '", save_path, "'")

end = time.time()
print("\n> Elapsed time:", from_seconds_to_elapsed_time(end - start))

# NOTE

# This code is meant to be executed once
# It creates a .csv with all the AGGIUDICATARI, which is then uploaded to the MySQL DB (by script 2)

# To update the AGGIUDICATORI db, use script agg_03
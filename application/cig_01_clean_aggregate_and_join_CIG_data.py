from functions import *
import time

"""
# This code is meant to be executed once

# 1. It imports, cleans and merges all the CIG data
# 2. It imports the already cleaned AGGIUDICATARI data
# 3. It merges the data based on "cig"
# 4. It stores the data as .csv
"""

################
### SETTINGS ###
################

# Directory in which we find all the CIG .csv
cigs_path = "datasets/raw_data/cig/"

# Path of cleaned and merged AGGIUDICATARI .csv
aggs_path = "datasets/clean_data/elenco_aggiudicatari.csv"

# Directory in which we store the final .csv with the cleaned, merged and joined data
save_path = "datasets/clean_data/"

# Name of the final .csv
dataset_name = "appalti_aggiudicatari.csv"

##############
### SCRIPT ###
##############

# Tracking the time
start = time.time()

# Import, clean and merge all CIG data
print("\n> Importing all CIG datasets")
all_cigs_df = mergeCIG(cigs_path)
print("> All CIGs cleaned and saved into a dataframe")

# Import clean and already merged AGGIUDICATARI data
print("\n> Importing AGGIUDICATARI dataset")
all_aggs_df = importAggiudicatari(aggs_path)

# Join the data
print("\n> Joining the CIG and the AGGIUDICATARI dataset")
full_df = joinCIGAggiudicatari(all_cigs_df, all_aggs_df)
print("> Join performed correctly")

# Print some info on the data
print("\n> Dataset sample and information\n")
print(full_df.head())
print("\nTotal number of rows:", full_df.shape[0])

# Save the dataset as .csv
print("\n> Saving the dataset...")
full_df.to_csv(save_path + dataset_name, index = False, sep=";")
print("> Dataset correctly saved in '", save_path, "'")

# Calculate and print total time
end = time.time()
print("\n> Elapsed time:", from_seconds_to_elapsed_time(end - start))
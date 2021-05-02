from functions import *
import time

"""
# This code is meant to be executed once
# It creates a clean .csv with all the AGGIUDICATARI data
"""

################
### SETTINGS ###
################

# Directory in which we find all the AGGIUDICATARI .csv
agg_path = "datasets/raw_data/aggiudicatari/"

# Directory in which we store the final .csv with the cleaned and merged data
save_path = "datasets/clean_data/"

# Name of the final .csv
final_csv_name = "elenco_aggiudicatari.csv"

##############
### SCRIPT ###
##############

# Tracking the time
start = time.time()

# Import, clean and merge all AGGIUDICATARI data
print("\n> Importing all AGGIUDICATARI datasets")
all_agg_df = mergeAggiudicatari(agg_path)
print("> All AGGIUDICATARI cleaned and saved into a dataframe")

# Print some info on the clean data
print("\n> Dataset sample and information\n")
print(all_agg_df.head())
print("\nTotal number of rows:", all_agg_df.shape[0])

# Save the dataset as .csv
print("\n> Saving the dataset...")
all_agg_df.to_csv(save_path + final_csv_name, index = False, sep=";")
print("> Dataset correctly saved. Directory:", save_path)

# Calculate and print total time
end = time.time()
print("\n> Elapsed time:", from_seconds_to_elapsed_time(end - start))
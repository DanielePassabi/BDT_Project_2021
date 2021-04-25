from functions import *
import time

start = time.time()

print("\n> Importing all CIG datasets")
cigs_path = "datasets/cig/"
all_cigs_df = mergeCIG(cigs_path)
print("> All CIGs cleaned and saved into a dataframe")

print("\n> Importing all AGGIUDICATARI datasets")
aggs_path = "datasets/aggiudicatari/"
all_aggs_df = mergeAggiudicatari(aggs_path)
print("> All AGGIUDICATARI cleaned and saved into a dataframe")

print("\n> Joining the CIG and the AGGIUDICATARI dataset")
full_df = joinCIGAggiudicatari(all_cigs_df, all_aggs_df)
print("> Join performed correctly")

print("\n> Dataset sample and information\n")
print(full_df.head())

print("\nTotal number of rows:", full_df.shape[0])

print("\n> Saving the dataset...")

save_path = "datasets/clean_data/"
dataset_name = "full_dataset.csv"

full_df.to_csv(save_path + dataset_name, index = False, sep=";")

print("> Dataset correctly saved in '", save_path, "'")

end = time.time()
print("\n> Elapsed time:", from_seconds_to_elapsed_time(end - start))
from functions import *
import time

# Tracking the time
start = time.time()

print("\n> Updating AGGIUDICATARI datasets")

# TODO: chiedere come si può fare in modo rapido
#  
# > viene fornito un unico csv
# > bisogna inserire su MySQL solo le righe nuove
# >> è necessario provare a inserirle tutte (1.7M)?
# >> esiste un metodo più rapido? 

# OPZIONE 1
# A. troncare il database esistente
# B. inserire i nuovi dati degli AGGIUDICARI

# OPZIONE 2 <-- 
# A. ottenere i dati già presenti nel bd
# B. fare un confronto con i nuovi dati
# C. aggiungere solo i nuovi dati
# comporta avere entrambi i dataset in memoria











# calculate and print total time
end = time.time()
print("\n> Elapsed time:", from_seconds_to_elapsed_time(end - start))
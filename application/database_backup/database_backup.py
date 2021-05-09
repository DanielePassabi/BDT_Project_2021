# necessary to import other modules
import sys
sys.path.append('../')

from config import *

import os
import time
import datetime
import pipes
 
################
### SETTINGS ###
################

# Paths
backup_dir_path = paths["backup_dir_path"]

# MySQL credentials
host = mysql_credentials["host"]
database = mysql_credentials["database"]
user = mysql_credentials["user"]
password = mysql_credentials["password"]


##############
### SCRIPT ###
##############

# Getting current DateTime to create the separate backup folder like "20200509-155612".
current_date = time.strftime('%Y%m%d-%H%M%S')
backup_path = backup_dir_path + '/' + current_date
 
# Checking if backup folder already exists or not. If not exists will create it.
try:
    os.stat(backup_path)
except:
    os.mkdir(backup_path)
 
print ("> Starting backup of database " + database)

db = database
dumpcmd = "mysqldump -h " + host + " -u " + user + " -p" + password + " " + db + " > " + pipes.quote(backup_path) + "/" + db + ".sql"
os.system(dumpcmd)
 
print ("> Backup script completed")
print ("> Backup created in '" + backup_path + "' directory")
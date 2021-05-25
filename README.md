# BDT_Project_2021

Project of BDT - Giorgia Villa, Daniele Passabì

## Application

### *Description*

This code provides a possible implementation of a Big Data System able to preform predictions on tenders published by the Italian administrative bodies. It returns the most likely winners of a tender specified by the end-user through a customised interface. Predictions are based on historical data and obtained through a machine learning model running a K-NearestNeighbour classification.

### *How to start (end user)*

To the end-user it is simply required to run the respective file exe. This will open a window were some company and tender information need to be specified. Once done this, it is enough to click on the *Get prediction* button and the prediction for the most likely tender winner will be displayed.

### *How to start (developer) BLEAH* - DANI NO ME GUSTA, CI PENSO DOPO

The application runs autonomously after the execution of the proper exe file. Nevertheless, data have to be updated monthly.

- tenders data are updated monthly
- they are uploaded in the MySQL database
- the prediction model is trained also on the new data
- the application is updated and released to the user

### *Python requirements*

- Suggested Python version: X.Z
- Required libraries: the file `requirements.txt` contains all libraries to be installed for the application to run properly.

### *MySQL Requirements*

- It is necessary to install a MySQL instance, such as [MySQL Workbench](https://www.mysql.com/it/products/workbench/).
- In the chosen MySQL instance two tables must be generated, as follows:

<br/>
Table 1

Table Name:  `elenco_aggiudicatari`
| Column Name           | Column Type   |
|-----------------------|---------------|
| `cig`                 | CHAR(10)      |
| `aggiudicatario`      | VARCHAR(128)  |
| `tipo_aggiudicatario` | VARCHAR(256)  |

<br/>
Table 2

Table Name: `appalti_aggiudicatari`
| Column Name                                 | Column Type   |
|---------------------------------------------|---------------|
| `cig`                                       | CHAR(10)      |
| `numero_gara`                               | VARCHAR(10)   |
| `importo_complessivo_gara`                  | FLOAT         |
| `n_lotti_componenti`                        | SMALLINT      |
| `importo_lotto`                             | FLOAT         |
| `settore`                                   | VARCHAR(32)   |
| `data_pubblicazione`                        | DATE          |
| `tipo_scelta_contraente`                    | VARCHAR(128)  |
| `modalita_realizzazione`                    | VARCHAR(128)  |
| `denominazione_amministrazione_appaltante`  | VARCHAR(256)  |
| `sezione_regionale`                         | VARCHAR(32)   |
| `descrizione_cpv`                           | VARCHAR(256)  |
| `aggiudicatario`                            | VARCHAR(128)  |
| `tipo_aggiudicatario`                       | VARCHAR(256)  |

<br/>

Notes on column type choices: specific column types were chosen on the basis of the [Official Documentation](https://dev.mysql.com/doc/refman/8.0/en/floating-point-types.html) and on the specific type of variable present in each column. The aim was to minimize the required space, without preventing further developments of the application.

---

## Code Structure

Below the detailed description of the code structure of this project.

### *Database population*

In folder `database_population` there are two files.

- `config.py`, with configuration settings necessary to populate the database for the first time. In details in contains:
  - paths of folders of the csv files downloaded from ANAC official website, available at this [link](https://dati.anticorruzione.it/opendata/dataset?page=1).
  - Credentials of the MySQL database in which the cleaned data will be stored

- `populate_database.py` which:
  - takes the datasets in the *raw* folder in .csv format;
  - cleans aggiudicatari data and uploads them in the MySQL database;
  - cleans tenders data, joins them with the aggiudicatari data and uploads the results in the MySQL database.

This operation is thought to be performed only once. Data will be then updated through the application presented in the next paragraph.

### *Database update*

#### *Premise*

ANAC provides data on tenders (CIG) and on winners (aggiudicatari) differently:

- CIG: every month a new .csv is released with data related to tenders of that month.
- Winners: seldom the same .csv file is updated with new winners (hence the file is getting larger and larger).

For this reason two different procedures were implemented to update data on the MySQL database.

#### *Solution*

The MySQL database can be updated in two ways: through the application (suggested) o by running the Python scripts specifically for the tables in the database.

#### *Update though application*

- The application for update can be run through the script `update_database_interface.py`

- It lets the user select which kind of tables to update (`elenco_aggiudicatari` | `appalti_aggiudicatari`)

- It lets the user select the new .csv with raw data to be added to the MySQL database

- It lets the user provide their own MySQL credentials

- Once all information have been provided, it is only necessary to click on the *Update DB* button to launch the updating procedure.

- Below some pictures.

  TODO: INSERIRE IMMAGINE APPLICAZIONE

#### *Script Python*

First of all, it is necessary to provide credentials and settings for the MySQL database in the configuration file `config.py`.

Below a detailed explanation of the script and logic of the system:

- `update_database_CIG`
  - enables to update the table `appalti_aggiudicatari`
  - enables to select a new file .csv (raw) with new data concerning tenders
  - cleans the new data
  - updates the MySQL database

- `update_database_aggiudicatari_v1`
  - enables to update the table `elenco_aggiudicatari`
  - enables to select a new file .csv (raw) with new data concerning winners
  - removes old data about winners from the MySQL database
  - uploads the new data on the MySQL database

- `update_database_aggiudicatari_v2`
  - enables to update the table `elenco_aggiudicatari`
  - enables to select a new file .csv (raw) with new data concerning winners
  - compares the the new data with the ones already present in the MySQL database
  - updates the MySQL database loading only records not already present in the database

Note: `update_database_aggiudicatari_v1` is way less efficient and faster than `update_database_aggiudicatari_v2`. It is left as an alternative solution in case the dataset is too large to be stored twice in memory (which is necessary for the comparison operation).

### *Database backup*

In folder `database_backup` it is possible to run a script to generate a backup of the MySQL database.

In the `config.py`, it is possible to provide customized database settings and the folder in which to save the dump.

It is suggested to periodically dump files, possibly in clouds or on a different machine from the one with the original database.

### *Final App: Predict Tender Winner*

The final application is based on the following configuration files and scripts.

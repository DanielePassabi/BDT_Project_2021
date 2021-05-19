paths = dict(
    agg_dir_path = "../datasets_2_test/raw_data/aggiudicatari/",   # Directory in which we find all the AGGIUDICATARI .csv
    cig_dir_path = "../datasets_2_test/raw_data/cig/",             # Directory in which we find all the CIG .csv
    clean_data_dir_path = "../datasets_2_test/clean_data/",        # Directory in which we store the clean data
    clean_agg_csv_name = "elenco_aggiudicatari.csv",             # Name of the final AGGIUDICATARI .csv
    agg_cig_csv_name = "appalti_aggiudicatari.csv",              # Name of the final CIG AGGIUDICATARI.csv
)

mysql_credentials = dict(
    host = "127.0.0.1",
    port = 3306,
    database = "db_bdt_project",
    user = "root",
    password = "dany1998",
)


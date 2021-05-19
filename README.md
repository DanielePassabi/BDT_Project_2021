# BDT_Project_2021

Project of BDT - Giorgia Villa, Daniele Passabì

## Application

### *Description*

La nostra applicazione fa questo e questo.

### *How to start (end user)*

è semplicemente richiesto di eseguire il file exe, inserire le informazioni della propria azienda (e dell'asta) e cliccare il pulsante per ottenere la predizione della possibile azienda vincitrice.

### *How to start (developer)*

L'applicazione funziona in modo autonomo e presuppone di essere aggiornata mensilmente.

- i dati delle aste vengono aggiornati mensilmente
- vengono inseriti nel DB MySQL
- viene riaddestrato il modello di predizione
- viene aggiornata (e ripubblicata) l'applicazione

### *Python requirements*

- si consiglia l'uso di Python versione X.Z
- è presente un file `requirements.txt` con tutte le librerie necessarie al corretto funzionamento dell'applicazione

### *MySQL Requirements*

- è necessario installare un'instanza di MySQL, come ad esempio [MySQL Workbench](https://www.mysql.com/it/products/workbench/).

- è necessario creare due tabelle, con le seguenti caratteristiche:

<br/>

Table `elenco_aggiudicatari`
| Column Name           | Column Type   |
|-----------------------|---------------|
| `cig`                 | inserire tipo |
| `aggiudicatario`      | inserire tipo |
| `tipo_aggiudicatario` | inserire tipo |

<br/>

Table `appalti_aggiudicatari`
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

Note sulle scelte effettuate: è stato effettuato uno studio basato sulla [Official Documentation](https://dev.mysql.com/doc/refman/8.0/en/floating-point-types.html) e sullo specifico tipo di variabili contenute nelle colonne. Abbiamo puntato a ridurre lo spazio richiesto al minimo, ma senza sacrificare la futura espandibilità dell'applicazione.

---

## Code Structure

Segue la descrizione della struttura del codice del nostro progetto, con spiegazioni dettagliate.

### *Database population*

Nella cartella `database_population` si trovano due file.

- Il primo, `config.py`, contiene le informazioni di configurazione necessarie per popolare il database per la prima volta. Queste comprendono:
  - i path delle cartelle in cui vi sono i file .csv scaricati dal sito ufficiale dell'ANAC, reperibili a [questo](https://dati.anticorruzione.it/opendata/dataset?page=1) link.
  - i dati del database MySQL in cui i dati (puliti) verranno caricati

- Il secondo è lo script `populate_database.py`, che, a partire dai dataset *raw* in formato .csv:
  - pulisce i dati degli aggiudicatari e li carica sul db mysql
  - pulisce i dati degli appalti, esegue un join con i dati degli aggiudicatari e li carica sul db mysql

Questa operazione è pensata per essere eseguita una volta sola. I dati verranno poi aggiornati attraverso l'applicazione presentata nella prossima sezione.

### *Database update*

#### *Premise*

ANAC fornisce i dati rigurdanti gli appalti (CIG) e gli aggiudicatari in modo diverso:

- CIG: ogni mese viene rilasciato un nuovo .csv con i dati riguardanti le aste di quel mese.
- Aggiudicatari: in lassi di tempo molto più lunghi viene aggiornato lo stesso grande file .csv con nuovi aggudicatari

Questo ha reso necessario operare in due diversi modi per aggiornare le tabelle presenti nel nostro database MySQL.

#### *Solution*

è possibile aggiornare il database in due modi: usando l'applicazione (consigliata) o i singoli script Python specifici per le tabelle presenti nel database.

#### *Applicazione*

- Lanciabile attraverso lo script `update_database_interface.py`

- Permette di selezionare il tipo di tabella che si vuole aggiornare (`elenco_aggiudicatari` | `appalti_aggiudicatari`)

- Permette di selezionare il .csv contenente i raw data che si vogliono aggiungere al DB

- Permette di inserire le proprie credenziali MySQL

- Una volta inserite le informazioni, è semplicemente necessario cliccare su *Update DB* per avviare il processo di aggiornamento dei dati.

- Seguono delle immagini esplicative

  TODO: INSERIRE IMMAGINE APPLICAZIONE

#### *Script Python*

è presente un file di configurazione `config.py`, nel quale è necessario inserire le informazioni riguardanti il database MySQL.

Segue una spiegazione del funzionamento degli script:

- `update_database_CIG`
  - permette l'update della tabella `appalti_aggiudicatari`
  - permette di selezionare un nuovo file .csv (raw) con nuovi dati riguardanti gli appalti
  - i nuovi dati vengono puliti
  - il database viene aggiornato

- `update_database_aggiudicatari_v1`
  - permette l'update della tabella `elenco_aggiudicatari`
  - permette di selezionare un nuovo file .csv (raw) con nuovi dati riguardanti gli aggiudicatari
  - rimuove i vecchi dati riguardanti gli aggiudicatari dal database MySQL
  - aggiunge i nuovi dati

- `update_database_aggiudicatari_v2`
  - permette l'update della tabella `elenco_aggiudicatari`
  - permette di selezionare un nuovo file .csv (raw) con nuovi dati riguardanti gli aggiudicatari
  - confronta i dati già presenti nel db con i nuovi dati
  - aggiorna il db aggiungendo solo i nuovi dati

Note: `update_database_aggiudicatari_v1` è molto meno efficiente e veloce di `update_database_aggiudicatari_v2`. Viene lasciata come soluzione alternativa nel caso in cui il dataset dovesse essere troppo grande da non poter più essere contenuto (2 volte) in memoria, operazione necessaria per il confronto.

### *Database backup*

Nella cartella `database_backup` è possibile eseguire un semplice script per la creazione di un backup del proprio database MySQL.

Anche qui è presente un file di configurazione `config.py`, in cui è possibile settare le proprie informazioni rigurdanti il database e la cartella in cui salvare il dump.

è consigliato eseguire periodicamente il dump dei file, possibilmente in cloud o su una macchina diversa da quella che ospita il database originale.

### *Final App: Predict Tander Winner*

Qui sono presenti i file di configurazione e gli script su cui è basata l'applicazione finale.


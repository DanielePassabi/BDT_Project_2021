# Notes

## *Storico Lavoro*

- Esplorazione dei dati, volta a comprendere i dataset con cui dovremo lavorare
- Analisi più approfondita dei dati attraverso l'uso di KNIME
- Creazione di pipeline per puliza dei dati attraverso KNIME
- Studio di quali tecnologie è consono usare per risolvere al meglio il task del progetto
- Primi test con database MySQL
  - utilizzo di MySQL Workbench
  - connessione a MySQL DB attraverso Python
  - studio approfondito dei vari *data types*
  - test efficienza per creazione database
  - test efficienza per update database
  - creazione script per creazione, update e backup del database
  - creazione applicazione per update più veloce del database
- Studio di architetture Machine Learning (e non) per la risoluzione del task
- Implementazione e test di varie architetture 
- Creazione applicazione finale, basata sull'architettura scelta

---

## *Dati*

- I dati forniti da *ANAC* sono consistenti e ben fatti.
- [Link](https://dati.anticorruzione.it/opendata#HIDE1) alla descrizione del dataset.
- [Link](https://dati.anticorruzione.it/opendata/dataset?page=1) per download dei dataset.

---

## *Cose da ricordare*

### *Generali*

- È più facile che in certe zone vincano sempre le stesse aziende (ci sono vincitori storici), quindi utilizzare informazioni rigurdanti il luogo nel modello.
- Per quanto riguarda il dataset **Bando CIG**
  - La colonna `stato` non fornisce alcuna informazione utile. Si può dunque rimuovere (o non utilizzare per il modello ML)
  - Le colonne `luogo_istat` e `provincia` contengono per la maggior parte valori nulli. Non ci sono utili.
  - La colonne `codice_ausa` (che identifica univocamente `cf_amministrazione_appaltante` e `denominazione_amministrazione_appaltante`) presenta valori nulli. Non possiamo usarla, meglio usare direttamente il nome (`denominazione_amministrazione_appaltante`).
- Per quanto riguarda il dataset **AGGIUDICATARI**
  - *Mandante*: colui che da
  - *Mandatario*: chi si obbliga a compiere un'azione per conto del mandante

### *Consigli Professore*

- A chi è indirizzata?

  **R**: ad un ente economico che ha intenzione di partecipare alla gara di appalto.

- Qual è il fine?

  **R**: vedere la probabilità che date le sue caratteristiche/potenzialità il dato ente economico vinca il bando.

- Cosa vede ed usa l'utente? Un applicativo web? Un bot di Telegram? Un'applicazione? Come si usa?

  **R**: un'applicazione.

- Specificare per diversi tipi di bando. Per esempio: trasporti, edilizia scolastica, infrastrutture pubbliche (strade, ecc), servizi pubblici (monnezza, pulizia ospedali). Specificare anche per diverse regioni e/o città?

  Riusciamo ad addestrare il modello in base ai parametri proposti.

---

## *Cose da fare*

[X] refactoring database population

[X] refactoring database update

[X] provare a implementare la barra di progresso

[X] impostare la struttura del paper (tecnico)

[X] sistema di backup per MySQL

[X] provare soluzioni ML

- [Link](https://towardsdatascience.com/how-to-tackle-any-classification-problem-end-to-end-choose-the-right-classification-ml-algorithm-4d0becc6a295) utile per problemi di classificazione
- [Link](https://medium.com/@b.terryjack/tips-and-tricks-for-multi-class-classification-c184ae1c8ffc) utile per multi-class classification

[X] interfaccina per soluzione ML

[X] Pulizia dataset in seguito a nuove inconsistenze

[X] Per MySQL studiare in modo più approfondito il tipo delle colonne

[] Aggiungere file `requirements.txt` per INTERO PROGETTO

[] Rendere applicazione finale un `.exe`

[] Tradurre il `README.md`

[] Informarsi su altre tecnologie da usare

[] Controllare che i prof abbiamo accesso al codice (su Github)

[] Alla fine di tutto, correggere i path (da test a ufficiale)

## *Cose da fare (meno urgenti)*
[] aggiungere pulsante su interfaccia per fare backup dopo update

[] fare interfaccia per popolazione iniziale del db


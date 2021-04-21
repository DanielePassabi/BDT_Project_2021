# Storico Lavoro

## 21 Aprile 2021

- Esplorazione dei dati, volta a comprendere i dataset con cui dovremo lavorare
- Creazione dataset pulito e completo del 2020 per primi test
- Creazione cartella `application`, che conterrà la soluzione finale
- Creazione script `functions.py`, con funzioni per creare un modello basato su KNN in grado di predire il più probabile vincitore dell'asta

---

## *Dati*

- Quelli di ANAC sono fatti molto bene.

- Il prof ha parlato di CSV da 5 milioni di righe.

[Link alla descrizione del dataset](https://dati.anticorruzione.it/opendata#HIDE1)

[Link ai dataset](https://dati.anticorruzione.it/opendata/dataset?page=1)

---

## *Cose da ricordare*

<br>

Generali

- È più facile che in certe zone vincano sempre le stesse aziende (ci sono vincitori storici)

<br>

Per quanto riguarda il dataset **Bando CIG**
- La colonna `stato` non fornisce alcuna informazione utile. Si può dunque rimuovere (o non utilizzare per il modello ML)

- Le colonne `luogo_istat` e `provincia` contengono per la maggior parte valori nulli. Non ci sono utili.

- La colonne `codice_ausa` (che identifica univocamente `cf_amministrazione_appaltante` e `denominazione_amministrazione_appaltante`) presenta valori nulli. Non possiamo usarla, meglio usare direttamente il nome (`denominazione_amministrazione_appaltante`).

<br>

Per quanto riguarda il dataset **AGGIUDICATARI**
- *Mandante*: colui che da

- *Mandatario*: chi si obbliga a compiere un'azione per conto del mandante

---

## *Consigli Professore*

- A chi è indirizzata?

  R: ad un ente economico che ha intenzione di partecipare alla gara di appalto.

- Qual è il fine?

  R: vedere la probabilità che date le sue caratteristiche/potenzialità il dato ente economico vinca il bando.

- Cosa vede ed usa l'utente? Un applicativo web? Un bot di Telegram? Un'applicazione? Come si usa?
- Specificare per diversi tipi di bando. Per esempio: trasporti, edilizia scolastica, infrastrutture pubbliche (strade, ecc), servizi pubblici (monnezza, pulizia ospedali).
- Specificare per diverse regioni e/o città?

---

## *Cosa fare ora?*

[x] Che dati ci sono, come sono fatti, cosa ce ne dobbiamo fare?

[ ] Sistema ad alto livello: capire l'utente cosa vede e cosa fa.

[ ] Capire che architettura ML utilizzare per poter usare al meglio tutte le features.

[ ] Imparare a creare un'interfaccia grafica per l'applicazione.

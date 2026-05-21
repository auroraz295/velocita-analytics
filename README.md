# VeloCittà Analytics
##### *Aurora Zuccarello*

### Descrizione progetto
*VeloCittà Analytics* è un sistema di analisi dati end-to-end sviluppato per una startup italiana di bike sharing attiva nelle città di Milano, Roma e Torino.
Il progetto copre la *programmazione a oggetti*, l'analisi numerica con *NumPy*, la manipolazione dati con *Pandas* e la creazione di *grafici*.

### Istruzioni
- Installare i requisiti su *requirements.txt*
- Eseguire gli script nel seguente ordine:
  - demo.py
  - modulo_classi.py
  - modulo_numpy.py
  - modulo_pandas.py
  - modulo_visualizzazione.py

>Il file "teoria_sql.sql" contiene spiegazioni testuali teoriche su ipotetiche tabelle legate al progetto. 

### Visualizzazioni
Tutti i grafici ottenuti e la dashboard riepilogativa finale generati dagli script sono contenuti nella cartella */output*.

### Considerazioni
La difficoltà principale è stata la gestione di tanti punti diversi e lo "switch" mentale tra i vari paradigmi, passando dalla logica della programmazione a oggetti a quella dell'analisi numerica con NumPy e Pandas. 
Inoltre, ho trovato poco comodo dover inventare e generare dati randomici direttamente via codice per i DataFrame, così come la gestione dei grafici, operazione che trovo molto più immediata e comoda su strumenti dedicati come ad esempio Power BI. 

Per migliorare il progetto, sicuramente sarebbe un plus rendere "reale" un database su MySQL contenente i dati, oppure basarsi su un file esterno CSV. 

Un'interessante osservazione sui dati, ricavata dal *grafico 3 "Distribuzione delle corse per fascia oraria e tipologia mezzo"*, riguarda la differenza dell'utilizzo tra la bicicletta classica, fortemente preferita nelle fasce orarie *"mattina"* e *"notte"*, rispetto all'uso della bicicletta elettrica. 

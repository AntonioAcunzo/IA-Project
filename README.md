# Potatura di regole negli alberi di decisione

Il programma è stato inmplementato mediante il linguaggio di programmazione Python, versione 2.7 .
Il codice è ampiamente commentato, così da renderlo più leggibile ad un possibile utilizzatore.

## Guida all'utilizzo del programma
1. Procurarsi un dataset che sia in formato csv o txt ed inserirlo nella cartella del programma. È necessario modificare la variabile file_name all'inizio del file Main.py, inserendo il nome del database scelto. In alternativa utilizzare uno dei tre dataset già presenti nella cartella su cui sono stati effettuati gli esperimenti. 
2. Opzionale: inserire il numero di prove da effettuare modificando la variabile numTests all'inizio del file Main.py. Di default verranno eseguite 3 prove.
3. Eseguire il file Main.py che terminerà con la stampa dei test eseguiti a video e la visualizzazione di un instogramma.

Alcune osservazioni necessarie al funzionamento:
+ La prima riga del database deve contenere la lista degli attributi seguiti dal target, separati da una virgola.
+ Il target del dataset scelto deve essere un attributo di tipo booleano.
+ Il dataset non deve contenere attributi con dati mancanti.

Informazioni aggiuntive:
+ L'esperimento è stato eseguito su tre datasets presi dal repository [MLData](http://http://mldata.org/).


Per maggiori informazioni consultare la relazione associata.



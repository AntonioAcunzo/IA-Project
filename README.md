# Potatura di regole negli alberi di decisione

Il programma è stato implementato mediante il linguaggio di programmazione Python, versione 2.7 .
Il codice è ampiamente commentato, così da renderlo più leggibile ad un possibile utilizzatore.

## Guida all'utilizzo del programma
1. Procurarsi un dataset che sia in formato csv o txt ed inserirlo nella cartella del programma. In alternativa utilizzare uno dei tre dataset, presi dal repository [MLData](http://http://mldata.org/), già presenti nella cartella su cui sono stati effettuati gli esperimenti. In entrambi i casi è necessario modificare la variabile *file_name* all'inizio del file Main.py, inserendo il nome del database scelto.
2. Opzionale: inserire il numero di prove da effettuare modificando la variabile *numTests* all'inizio del file Main.py. Di default verranno eseguite 3 prove.
3. Eseguire il file Main.py che terminerà con la stampa dei test eseguiti in console e la visualizzazione di un instogramma.

*Nota: i tempi di esecuzione variano in base alla piattaforma di esecuzione, e al numero di record del dataset su cui si vuole effettuare l'esperimento.*

Alcune osservazioni necessarie al funzionamento:
+ La prima riga del database deve contenere la lista degli attributi seguiti dal target, separati da una virgola.
+ Il target del dataset scelto deve essere un attributo di tipo booleano.

Per maggiori informazioni consultare la relazione associata.

import pickle
from timeit import default_timer as timer

from DataSet import readDataset
from Learning import *



#Dataset

file_name = "breast_cancer_dataset.csv"
#file_name = "plant_classification_dataset.csv"
#file_name = "book_evaluation_dataset.csv"

print "-----------------------------------"
print "DATASET :", file_name

numTests = 2
print "Numero test da effettuare :", numTests

list = readDataset(file_name)
print "-----------------------------------"
attributes = list[0]

start = timer()

set = []
training_set = []
validation_set = []
test_set = []

avgAccOriginalTree_tr = 0
avgAccPrunedTree_tr = 0
avgAccOriginalTree_vs = 0
avgAccPrunedTree_vs = 0
avgAccOriginalTree_ts = 0
avgAccPrunedTree_ts = 0

for i in range(numTests):
    start1 = timer()
    print " - Esecuzione Test", i+1

    set = createSet(list[1])
    training_set = set[0]
    validation_set = set[1]
    test_set = set[2]

    #Applico l'algoritmo di apprendimento e creo l'albero di decisione
    root = id3(training_set, attributes)
    tree = Tree(root)

    #Trasformo l'albero in regole
    dnf_original_tree = DNF_tree(tree)

    results = pruning(dnf_original_tree, validation_set, training_set, attributes)

    avgAccOriginalTree_vs += results[0]
    dnf_pruned_tree = results[1]
    avgAccPrunedTree_vs += results[2]

    avgAccOriginalTree_tr += calculateAccuracy(createDataFrame(training_set,attributes),dnf_original_tree,attributes)
    avgAccPrunedTree_tr += calculateAccuracy(createDataFrame(training_set,attributes),dnf_pruned_tree,attributes)
    avgAccOriginalTree_ts += calculateAccuracy(createDataFrame(test_set,attributes),dnf_original_tree,attributes)
    avgAccPrunedTree_ts += calculateAccuracy(createDataFrame(test_set,attributes),dnf_pruned_tree,attributes)

    end1 = timer()
    print "Tempo esecuzione test", i+1 , ":", (end1-start1)

#Medie accuratezze
avgAccOriginalTree_tr /= numTests
avgAccPrunedTree_tr /= numTests

avgAccOriginalTree_vs /= numTests
avgAccPrunedTree_vs /= numTests

avgAccOriginalTree_ts /= numTests
avgAccPrunedTree_ts /= numTests

accuracies = [avgAccOriginalTree_tr,avgAccOriginalTree_vs,avgAccOriginalTree_ts,avgAccPrunedTree_tr,avgAccPrunedTree_vs,avgAccPrunedTree_ts]

#Stampe risultati finali
print "---------------------------------------------------------------------------"

print "MEDIE ACCURATEZZE SUI SET"
print " TRAINING SET : "
print "  Accuratezza albero originale : ", avgAccOriginalTree_tr , "%"
print "  Accuratezza albero potato : ", avgAccPrunedTree_tr , "%"
print " VALIDATION SET : "
print "  Accuratezza albero originale : ", avgAccOriginalTree_vs , "%"
print "  Accuratezza albero potato di ", " elementi : ", avgAccPrunedTree_vs , "%"
print " TEST SET : "
print "  Accuratezza albero originale : ", avgAccOriginalTree_ts , "%"
print "  Accuratezza albero potato : ", avgAccPrunedTree_ts , "%"

end = timer()
print "TEMPO ESECUZIONE TOTALE:", (end-start)

graph(accuracies)




















''' COME FUNZIONA LA STRATEGIA DI PRUNING :

esempio:
A e B e C --> si
A e D --> no
B e E -->  no

prima provo a togliere A , e calcolo il delta cioe' la percentuale di miglioramento dell'accuratezza
torno a regole di partenza e provo a togliere B, e calcolo il delta cioe' la percentuale di miglioramento dell'accuratezza
C, A (seconda regola), D, B e E (terza regola)
controllo quale attributo porta al delta migliore --> migliore accuratezza
tolgo quell'attributo in quella regola e parto da capo
mi fermo quando non ho piu' miglioramenti.


oppure potrei fare la variante che se levo A dalla prima lo levo anche dalla seconda ...
'''

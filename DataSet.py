from random import shuffle
from timeit import default_timer as timer


#Funzione per prendere gli esempi da un file
#input : nome file
#output : lista attributi, lista esempi
def readDataset(file_name):

    start = timer()
    file = open(file_name,"r")

    #la prima fila contiene gli attributi separati da una virgola
    a = file.readline()
    attributes = str(a).strip().split(",")

    #Scorro le righe del file (ogni riga corrisponde ad un esempio) e le inseriso nella lista degli esempi
    examples = []
    for line in file:
        fields = line.strip().split(",")
        examples.append(fields)

    file.close()
    end = timer()
    print "Tempo lettura file: ", (end-start)

    return attributes,examples

#Funzione che divide l'insieme di esempi in training set, validation set e test set
#input : lista esempi da cui ricavare i tre set
#output : training set, validation set e test set
def createSet(examples):

    shuffle(examples)

    dim_tv = int(round(float(examples.__len__())*2/3))
    dim_train = dim_tv * 2/3
    dim_val = dim_tv * 1/3
    dim_test = examples.__len__() - dim_tv

    training_set = []
    validation_set = []
    test_set = []

    #creo training_set
    for i in examples[:dim_train]:
        training_set.append(i)

    #creo validation_set
    for i in examples[dim_train:dim_train+dim_val]:
        validation_set.append(i)

    #creo test_set
    for i in examples[dim_train+dim_val:dim_train+dim_val+dim_test]:
        test_set.append(i)

    return training_set, validation_set, test_set

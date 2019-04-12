import math
import copy
from timeit import default_timer as timer
from DataSet import *
from DataStructure import *

import matplotlib.pyplot as plt

import pandas as pd

#Funzione che restituisce tutti i possibili valori che l'attributo passato come parametro puo' assumere
# input : lista attributi, attributo e lista esempi
# output : lista dei possibili valori dell'attributo
def values(list_attributes, attribute, examples):
    values = []
    if not list_attributes.__len__() == 0 :
        for i in examples:
            if not i[list_attributes.index(attribute)] in values:
                values.append(i[list_attributes.index(attribute)])
    return values

#Funzioni per il calcolo dell'entropia
#Entropia 0 se tutti gli esempi sono della stessa classe (tutti +)
#Entropia 1 se tutti gli esempi sono perfettamente bilanciati

#Funzione che calcola l'entropia dell'insieme degli esempi
def entropyS(list_attributes, examples):
    attribute = list_attributes[list_attributes.__len__()-1]
    entropy = 0
    listD = []
    for i in examples:
        listD.append(i[list_attributes.index(attribute)])
    listND = values(list_attributes, attribute, examples)
    for i in listND:
        p = listD.count(i)/float(listD.__len__())  # quante volte compare quel risultato /  totale dei risultati
        entropy += -p * math.log(p, 2)
    return entropy

#Funzione che calcola l'entropia dopo aver assegnato ogni possibile valore dell'attributo passato in input
def entropyV(list_attributes, attribute, examples):
    e = []
    listD = []
    entropyTot = entropyS(list_attributes, examples)
    e.append(entropyTot)
    for i in examples:
        listD.append(i[list_attributes.index(attribute)])
    for i in values(list_attributes, attribute, examples):
        p1 = listD.count(i)/float(listD.__len__())  #occorrenze valore / insieme di esempi
        listTargetD = []  #lista target associati a quel valore con duplicati
        listTargetND = []     #lista target associati a quel valore senza duplicati
        for j in examples:
            if (j[list_attributes.index(attribute)] == i):
                listTargetD.append(j[len(j)-1])
                if not(j[len(j)-1] in listTargetND):
                    listTargetND.append(j[len(j)-1])

        #Calcolo entropia di ogni possibile valore
        total = 0
        for z in listTargetND:
            p = listTargetD.count(z)/float(listTargetD.__len__())
            entropy = -p * math.log(p, 2)
            total += p1 * entropy
        e.append(total)

    return e

#Funzione che calcola l'information gain di un attributo
# input : lista attributi, attributo di cui calcolare l'information gain e lista esempi
# output : information gain dell'attributo passato come parametro
def gain(list_attributes, attribute, examples):
    entropyValues = entropyV(list_attributes, attribute, examples)
    gain = entropyValues[0]
    for i in entropyValues[1:]:
        gain -= i
    return gain

#Funzione che trova e restituisce l'attributo con maggiore information gain
# input : lista attributi e lista esempi
# output : attributo con maggiore information gain
def importance(list_attributes, examples):
    gains = []
    max = float("-inf")
    for i in list_attributes[:len(list_attributes)-1]:
        if i == None :
            gains.append(-float("inf"))
        else :
            gains.append(gain(list_attributes, i, examples))
    for i in gains:
        if(i>max):
            max = i
    return list_attributes[gains.index(max)]

#Funzione che trova il valore di maggioranza del target degli esempi
# input : lista attributi, lista esempi e target
# output : valore piu' frequente del target
def valueMax(attributes, examples, attribute):
    if not examples.__len__() == 0:
        list = values(attributes,attribute,examples)
        cont_list = []
        for i in list:
            cont = 0
            for j in examples:
                if (j[j.__len__()-1]) == i:
                    cont += 1
            cont_list.append([i,cont])
        common = cont_list[0]
        for i in cont_list:
            if common[1] < i[1] :
                common = i
        return common
    else :
        common = "Default"

#Funzione per l'apprendimento dell'albero di decisione --> Algoritmo ID3
# input : lista attributi e lista esempi
# output : nodo radice dell'albero che verra' costruito successivamente
def id3(examples,attributes):

    #Creo radice dell'albero
    root = Node(None,None)

    #CASO 1/2: verifico se tutti gli esempi hanno stesso target (positivo o negativo)
    equal = True
    target_index = attributes.__len__()-1
    if not attributes.__len__() == 0:
        list_target = values(attributes,attributes[target_index],examples)
        if not(list_target.__len__() == 1):
            equal = False
        if(equal):
            root.name = list_target[0]
            root.label = None
            root.setLeaf(True)
            return root
        else :
            cont_target = []
            for i in list_target:
                cont_target.append(0)
                for j in examples:
                    if (j[target_index]) == i:
                        cont_target[list_target.index(i)] += 1
            common = 0
            for i in cont_target:
                if common < i :
                    common = i
            common_target = list_target[cont_target.index(common)]

    #CASO 4 : verifico se insieme di attributi vuoto
    numNone = 0
    for i in attributes:
        if i == None:
            numNone +=1
    if numNone == attributes.__len__()-1 or attributes.__len__()==0:
        root.name = common_target
        root.label = None
        return root

    a = importance(attributes, examples)
    root.name = a

    for i in values(attributes, a, examples):
        subset_examples = []

        figlio = Node(None,None)

        for j in examples:
            if( j[attributes.index(a)] == i):
                subset_examples.append(j)

        list = []
        for z in attributes:
            list.append(z)
        indice = list.index(a)
        list[indice] = None
        sub_tree = Node(None,None)

        if subset_examples.__len__() == 0:
            root.name = common_target
            root.label = None
            root.setLeaf(True)
            return root

        #Richiamo l'algoritmo di learning con
        # - nuova lista di attributi (tolgo l'attributo con maggiore gain)
        # - nuova lista di esempi (prendo solo gli esempi con il valore scelto dell'attributo con maggiore information gain)
        sub_tree = id3(subset_examples, list)

        figlio = sub_tree

        figlio.setLabel(i)
        root.children.append(figlio)
        figlio.p = root

    return root

#Funzione che dato un nodo risale l'albero fino alla radice memorizzando il cammino
#input: nodo foglia da cui risalire
#output: percorso da radice a foglia passata in iput
def gotoRoot(node):
    path = []
    path.append(node.name)
    father = node.p
    list = [father.name,node.label]
    path.append(list)
    while not father.p == None:
        list = [father.label]
        father = father.p
        list.append(father.name)
        list = list[::-1]
        path.append(list)
    path = path[::-1]
    return path

#Funzione che dato un albero restituisce la lista dei cammini da radice a foglia, trasforma l'albero in DNF.
#input: albero
#output: lista cammini da radice a foglia
def DNF_tree(tree):
    start = timer()
    paths = []
    for i in tree.nodes:
        if i.isLeaf == True:
            paths.append(gotoRoot(i))
    end = timer()
    print "Tempo per trasformare l'albero in dnf :", (end-start)
    print "Numero regole:",len(paths)
    return paths

#Funzione che rappresenta l'insieme passatogli in input con un DataFrame
#input: insieme di esempi, lista attributi
#output : dataframe
def createDataFrame(set,attributes):
    df = pd.DataFrame()
    array = []
    for i in attributes:
        for j in set:
            array.append(j[attributes.index(i)])
        df[i] = array
        array = []
    return df

#Funzione che calcola l'accuratezza delle regole passate in input sul dataframe di esempi
#input: dataframe, lista regole, lista attributi
#output : accuratezza
def calculateAccuracy(df,rules,attributes):
    df1 = copy.deepcopy(df)
    tests = len(df)
    corretti = 0
    for i in rules:
        correct_examples = calculate(df1,i,attributes)
        corretti += len(correct_examples)
        df1 = df1.drop(correct_examples.index, axis=0)
    accuracy = round((float(corretti)/tests)*100,2)
    return accuracy

#Funzione che crea un dataframe con gli esempi classificati correttamente dalla regola passata in input
#input: dataframe, regola, lista attributi
#output : dataframe
def calculate(df, rule, attributes):
    target = attributes[attributes.__len__()-1]
    for j in rule:
        if not j == rule[rule.__len__()-1]:
            df = df[df[j[0]]==j[1]]
            if df.empty :
                return df
        else:
            df = df[df[target] == j]
    return df

#Funzione che effettua la potatura delle regole passate in input
#input: lista regole, validation set, training set, lista attributi
#output : accuratezza regole originali, regole potate, accuratezza regole potate
def pruning(rules, validation_set, training_set, attributes):
    improved = True
    cont = 0
    start = timer()
    df_val = createDataFrame(validation_set,attributes)
    df_train = createDataFrame(training_set,attributes)
    accuracy_original = calculateAccuracy(df_val,rules,attributes)
    accuracy_pruned = accuracy_original
    while improved:
        cont+=1
        result = tryPruning(df_val,rules,attributes,accuracy_pruned)
        rules = result[0]
        accuracy_pruned = result[1]
        improved = result[2]
        #Criterio 2 di arresto : termino la potatura se l'accuratezza sul validation set supera quella sul training set
        accuracy_training_set = calculateAccuracy(df_train,rules,attributes)
        if accuracy_pruned>=accuracy_training_set:
            improved = False

    end = timer()
    print "Tempo potatura albero:", (end-start)
    print "Numero potature :" , cont-1
    return [accuracy_original,rules,accuracy_pruned]

#Funzione che effettua la potatura delle regole passate in input
#input: lista regole, lista attributi, accuratezza da migliorare
#output : regole potate, nuova migliore accuratezza, attributo che ci dice se effettivamente e' miglioramenta l'accuratezza
def tryPruning(df,rules,attributes,accuracy):
    start = timer()
    copy_rules = copy.deepcopy(rules)
    list_delta = []
    improved = False
    best_accuracy = accuracy

    for i in rules :
        index_rule = rules.index(i)  #indice della regola in copy_rules
        position_target = i.__len__()-1

        for k in i[:position_target]: #ciclo su tutti gli elementi e provo a potarne uno alla volta
            copy_rule = copy.deepcopy(i)
            copy_rules = copy.deepcopy(rules)
            if copy_rule.__len__() > 2:
                copy_rule.remove(k)  #rimuove elemento da regola
                copy_rules[index_rule] = copy_rule   #modifico la regola nella lista delle regole
                #Elimino le regole duplicate
                prec_index = None
                for y in copy_rules[::-1]:
                    if y == copy_rules[index_rule]:
                        if prec_index is not None:
                            copy_rules.remove(copy_rules[prec_index])
                        prec_index = copy_rules.index(y)
            else:
                copy_rules.remove(copy_rules[index_rule])

            accuracy = calculateAccuracy(df,copy_rules,attributes)
            list_delta.append([index_rule,k,accuracy])

    #Trovo potatura che porta a maggiore accuratezza
    for i in list_delta:
        if best_accuracy <= i[2]:
            best_prune = i
            best_accuracy = i[2]
            improved = True

    copy_rules = copy.deepcopy(rules)

    #Apporto la modifica alla regola
    if improved :
        if copy_rules[best_prune[0]].__len__() > 2 :
            copy_rules[best_prune[0]].remove(best_prune[1])
            #Cerco duplicati in lista e lascio quello piu' in alto
            prec_index = None
            for y in copy_rules[::-1]:
                if y == copy_rules[best_prune[0]]:
                    if prec_index is not None:
                        copy_rules.remove(copy_rules[prec_index])
                    prec_index = copy_rules.index(y)
        else:
            copy_rules.remove(copy_rules[best_prune[0]])
    else: #Criterio arresto 1
        print "Nessun miglioramento trovato"

    end = timer()
    return [copy_rules,best_accuracy,improved]


#Funzione che rappresenta i valori medi delle accuratezze in un istogramma
#input : accuratezze pre e post pruning sui tre data set
def graph(accuracies):

    plt.ylim(0,100)
    plt.bar([0, 1, 2, 4, 5, 6], accuracies,
    tick_label=["Training","Validation","Test","Training","Validation","Test"])
    plt.title("Accuracy Pre-Post Pruning")
    plt.xlabel("Decision Tree                                      Pruned Tree")
    plt.ylabel("Accuracy")
    plt.show()
    plt.savefig("./graph.png", dpi=72)

    return



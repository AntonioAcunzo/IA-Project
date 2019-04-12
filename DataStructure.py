class Node:

    def __init__(self,name,label):
        self.p = None
        self.name = name
        self.label = label
        self.children = []
        self.isLeaf = False

    #metodi set
    def setP(self,p):
        self.p = p;
    def setLabel(self,label):
        self.label = label;
    def setName(self,name):
        self.name = name
    def setLeaf(self,isLeaf):
        self.isLeaf = isLeaf

    def print_node(self):
        print str(self.name) + " , " + str(self.label) + " , " + str(self.isLeaf) + " --> " + str(self)
        print "     padre : " + str(self.p)
        if not self.children.__len__() == 0:
            for i in self.children:
                print "     figlio : " + str(i.name)
        else:
            print "     No figli"

class Tree:

    def __init__(self):
        self.root = None
        self.nodes = []
    def __init__(self,radice):
        self.root = radice
        self.nodes = []
        self.nodes.append(radice)
        self.build_tree(radice)

    def build_tree(self,root):
        for i in root.children:
            self.nodes.append(i)
            self.build_tree(i)

    def print_tree(self):
        print "------------------------Albero fatto da", self.nodes.__len__() , "nodi : -----------------------------------"
        self.print_subTree(self.root)
        print "------------------------------------------------------------------------------------------------------------"
    def print_subTree(self,root):
        root.print_node() #stampo radice
        for i in root.children:
            self.print_subTree(i)
            print "Torno al livello superiore"


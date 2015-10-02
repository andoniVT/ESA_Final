'''
Created on 1/10/2015

@author: ucsp
'''
from Test.xmlReader import Reader
from Test.TextCleaner import TextCleaner
from Test.VectorModel import VectorModel as VM
from Test.Utils import write_data_to_disk , load_data_from_disk , expand 
from Test.Classifier import SupervisedClassifier as SC
from Test.unsupervisedClassifier import Unsupervised

simpleVectorizer = "Models/simpleVectorizer.pk1"
tfidfModel = "Models/tfidfModel.pk1"
tfidfVectorizer = "Models/tfidfVectorizer.pk1"

SVM = "Classifiers/SVM.pk1"
NB = "Classifiers/NB.pk1"
ME = "Classifiers/ME.pk1"
DT = "Classifiers/DT.pk1"


corpusTrain1 = "Corpus/socialtv-tweets-train-tagged.xml"
corpusTrain2 = "Corpus/stompol-tweets-train-tagged.xml"
corpusTest1 = "Corpus/socialtv-tweets-train-tagged.xml"


class Manager(object):
    
    def __init__(self):
        pass
    
    def procesar(self, file, type):
        if type == 1:
            comentarios = []
            obj = Reader(file, 1)
            for i in obj.read():
                for j in i:
                    proc = TextCleaner(j[0])
                    value = [proc.get_processed_comment() , j[2]]
                    if value[0] != "None!":
                        comentarios.append(value)
            return comentarios
        else:
            pass
        
    
    def prepareModels(self, xml_file, type):
        comentarios = self.procesar(xml_file, type)
        train = []
        for i in comentarios:
            train.append(i[0])
        
        model = VM(train)
        vectorModelData = model.prepare_models()
        modelVectorizer = vectorModelData[0]
        modelVectorizerTFIDF = vectorModelData[1]
        modelTFIDF = vectorModelData[2]
        
        write_data_to_disk(simpleVectorizer, modelVectorizer)
        write_data_to_disk(tfidfVectorizer, modelVectorizerTFIDF)
        write_data_to_disk(tfidfModel, modelTFIDF)
                
    def trainClassifiers(self, xml_file, type):
        self.prepareModels(xml_file, type)
        comentarios = self.procesar(xml_file, type)
        data = load_data_from_disk(tfidfModel)
        data_expanded = []
        for i in data:
            vec = expand(i) 
            data_expanded.append(vec)
        labels = []
        for i in comentarios:
            labels.append(i[1])
        fileClassifiers = [SVM, NB, ME, DT]
        for i in range(4):
            classifier = SC(data_expanded, labels, i+1)
            fClass = classifier.train()
            write_data_to_disk(fileClassifiers[i], fClass)
    
    def test(self, comments, type):
        vectorizer = load_data_from_disk(simpleVectorizer)
        transformer = load_data_from_disk(tfidfVectorizer)
        model = VM()
        model.set_models(vectorizer, transformer)
                        
        if type == 1:
            return self.__testSVM(comments, model)
                        
        '''    
        elif type == 2:
            return self.__testNB(comments)
        elif type == 3:
            return self.__testME(comments)
        elif type == 4:
            return self.__testDT(comments)
        elif type == 5:
            return self.__testUnsup(comments)
        '''
    
    def __testSVM(self, comments, model):
        for i in comments.items():
                comentario = i[0]
                for j in i[1].items():
                    print j        
    
    def __testNB(self, comments):
        pass
    
    def __testME(self, comments):
        pass
    
    def __testDT(self, comments):
        pass
    
    def __testUnsup(self, comments):
        obj = Unsupervised(comments)
        return obj.classify()
    
    


if __name__ == '__main__':
    
    comments = ["es muy bonito" , "no es muy bonito"]
    
    obj = Manager()
    #obj.trainClassifiers(corpusTrain2, 1)
    
    #lista = {}
    #lista["Jorge es muy bonito"] = 2
    
    
    actores = {}
    actores["Jorge"] = 0
    actores["Andoni"] = 5
    
    actores2 = {}
    actores2["Valverde"] = 1
    actores2["Tohalino"] = 4
    
    comentarios = {}
    comentarios["hola como estas"] =  actores
    #comentarios["este es otro comentario"] = actores2
    
    
    
    obj.test(comentarios, 1)
    
    
    
    

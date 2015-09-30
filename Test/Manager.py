'''
Created on 15/8/2015

@author: andoni
'''
from Test4.xmlReader import Reader
from Test4.TextCleaner import TextCleaner
from Test4.VectorModel import VectorModel as VM
from Test4.Utils import write_data_to_disk , load_data_from_disk , expand 
from Test4.Classifier import SupervisedClassifier as SC
from Test4.dbConnection import Connection
from Test4.unsupervisedClassifier import Unsupervised as VocAlg
from Test4.entityManager import EManager as EM

simpleVectorizer = "Models/simpleVectorizer.pk1"
tfidfModel = "Models/tfidfModel.pk1"
tfidfVectorizer = "Models/tfidfVectorizer.pk1"

SVM = "Classifiers/SVM.pk1"
NB = "Classifiers/NB.pk1"
ME = "Classifiers/ME.pk1"
DT = "Classifiers/DT.pk1"




xml = "stompol-tweets-train-tagged.xml"
xmlTest = "testFile.xml"



corpusTrain1 = "Corpus/socialtv-tweets-train-tagged.xml"
corpusTrain2 = "Corpus/stompol-tweets-train-tagged.xml"
corpusTest1 = "Corpus/socialtv-tweets-train-tagged.xml"
corpusTest2 = "Corpus/socialtv-tweets-test.xml"


class SentimentManager(object):
    
    def __init__(self):
        self.__eManager = EM()
    
    def procesar(self, xml_file):
        comentarios = []
        obj = Reader(xml_file, 1)
        for i in obj.read():
            for j in i:
                proc = TextCleaner(j[0])
                value = [proc.get_processed_comment() , j[2]]
                comentarios.append(value)
        return comentarios  
                 
    
    def prepareModels(self, xml_file):
        comentarios = self.procesar(xml_file)
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
    
    def trainClassifiers(self, xml_file):
        comentarios = self.procesar(xml_file)
        
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
    
    def testClassifiers(self, test_data):        
        vectorizer = load_data_from_disk(simpleVectorizer)
        transformer = load_data_from_disk(tfidfVectorizer)
        model = VM()
        model.set_models(vectorizer, transformer)
        fileClassifiers = [SVM, NB, ME, DT]
        all_labels_predicted = []
        obj = Reader(test_data, 2)
        comentarios = obj.read()
        for i in comentarios:
            for j in i:
                entidad = j[1]                
                self.__eManager.add_entities(entidad) 
                comentario = j[0]
                supClass = load_data_from_disk(SVM)
                classifier = SC()
                classifier.set_classifier(supClass)
                proc = TextCleaner(comentario)
                text_cleaned =  proc.get_processed_comment()
                vector = model.get_comment_tf_idf_vector([text_cleaned])                
                result = classifier.classify(vector)
                polaridadSup =  result[0][0]
                
                voc =  VocAlg([comentario])
                polaridadNSup =  voc.classify()[0]
                 
                print " "
                
                self.__eManager.add_atributte(entidad, text_cleaned, polaridadSup, 1)
                self.__eManager.add_atributte(entidad, text_cleaned, polaridadNSup, 2)
            
    def test_comment(self, comentario):
        pass 
        
                         

if __name__ == '__main__':
    
    #obj = SentimentManager()
    #obj.prepareModels(xml)
    #obj.trainClassifiers(xml)
    
    #obj.testClassifiers(xmlTest)
    obj = Reader(corpusTrain2, 1)
    for i in obj.read():
        for j in i:
            print j 
    
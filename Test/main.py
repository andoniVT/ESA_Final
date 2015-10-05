#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
from Test.segmentation import Segmentation
from Test.commentPreprocessor import Comment_proccesor as CP
from nltk.test.unit.test_classify import RESULTS

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
    
    def test(self, comment, type):
        vectorizer = load_data_from_disk(simpleVectorizer)
        transformer = load_data_from_disk(tfidfVectorizer)
        model = VM()
        model.set_models(vectorizer, transformer)
        comentario = comment[0]
        seg = Segmentation(comentario)
        segmentos = seg.find_sentences()
        entities = comment[1].items()
        print segmentos
        
        if type == 1:
            return self.__testClassifier(segmentos, entities, model, SVM)                                    
        elif type == 2:
            return self.__testClassifier(segmentos, entities, model, NB)
        elif type == 3:
            return self.__testClassifier(segmentos, entities, model, ME)
        elif type == 4:
            return self.__testClassifier(segmentos, entities, model, DT)        
        elif type == 5:
            return self.__testUnsup(segmentos, entities)
        
    
    def __testClassifier(self, segmentos, entities, model, fileClass):
        results  = []                                                
        for j in segmentos:
            proc = TextCleaner(j)
            procesado = proc.get_processed_comment()
            
            vector = model.get_comment_tf_idf_vector([procesado])
            supClass = load_data_from_disk(fileClass)
            classifier = SC()
            classifier.set_classifier(supClass)
            result = classifier.classify(vector)
                      
            polaridadSup =  result[0][0]            
            for i in entities:                
                if j.find(i[0])!=-1:
                    value = (i[0] , polaridadSup)
                    results.append(value)        
        return results 
                                                                                                             
    
    
    def __testUnsup(self, segmentos, entities):
        results = []
        for i in segmentos:                    
            obj = Unsupervised(i)
            result = obj.classify()
            
            for j in entities:
                if i.find(j[0])!=-1:
                    value = (j[0], result)
                    results.append(value)
        return results 
    
    


if __name__ == '__main__':
    
    comments = ["es muy bonito" , "no es muy bonito"]
    
    obj = Manager()
    #obj.trainClassifiers(corpusTrain2, 1)
    
     
    
    actores = {}
    actores["Barcelona"] = 3
    actores["Madrid"] = 65
    
    comentario = {}
    #comentario["El Barcelona gana un titulo y es una temporada mediocre, el Madrid gana una copa y es un temporadon!!"] =  actores
    #comentarios["este es otro comentario"] = actores2
    comentario = ("El Barcelona gana un titulo y es una temporada mediocre, el Madrid gana una copa y es un temporadon!!" ,  actores)
    
    
    actores2 = {}
    actores2["Real Madrid"] = 18
    actores2["Barza"] = 65
    comentario2 = ("Felicitaciones al Real Madrid, en las buenas y en las malas Visca Barza!", actores2)
    
    
    actores3 = {}
    actores3["F.C Barcelona"] = 18
    actores3["Pinto"] = 23
    actores3["Real Madrid"] = 25
    actores3["Benzema"] = 35
    comentario3 = ("El mejor del F.C Barcelona en la final en mi opinión fue Pinto, el mejor del Real Madrid aunque no marcó fue Benzema, tiene mucha calidad.", actores3)
    
    
    
    results = obj.test(comentario3, 5)    
    for i in results:
        print i 
    
    
    
    
    
    
    

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

class Manager(object):
    
    def __init__(self):
        pass 
    
    def trainClassifiers(self, corpus_data=""):
        pass
    
    def test(self, comments, type):
        if type == 1:
            return self.__testSVM(comments)
        elif type == 2:
            return self.__testNB(comments)
        elif type == 3:
            return self.__testME(comments)
        elif type == 4:
            return self.__testDT(comments)
        elif type == 5:
            return self.__testUnsup(comments)
    
    def __testSVM(self, comments):
        pass
    
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
    print obj.test(comments, 5)

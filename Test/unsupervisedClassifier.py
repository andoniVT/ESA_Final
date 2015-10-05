'''
Created on 14/8/2015

@author: ucsp
'''
 
from Test.classifier import Classifier


class Unsupervised(object):
    
    def __init__(self, comment):
        self.__comment = comment
        self.__obj = Classifier()
    
    def classify(self):                
        self.__obj.classify(self.__comment)            
        return self.__obj.get_label() 

if __name__ == '__main__':
    
    comments = ["es muy bonito" , "no es muy bonito"]
    obj = Unsupervised(comments[1])
    print obj.classify()
    
    
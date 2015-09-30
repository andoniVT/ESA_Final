'''
Created on 14/8/2015

@author: ucsp
'''
 
from Test4.classifier import Classifier


class Unsupervised(object):
    
    def __init__(self, comments):
        self.__comments = comments
        self.__obj = Classifier()
    
    def classify(self):
        result = []
        for i in self.__comments:    
            self.__obj.classify(i)
            result.append(self.__obj.get_label())
        return result 

if __name__ == '__main__':
    
    comments = ["es muy bonito" , "no es muy bonito"]
    obj = Unsupervised(comments)
    print obj.classify()
    
    
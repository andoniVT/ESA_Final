'''
Created on 13/8/2015

@author: ucsp
'''
from Test4.commentPreprocessor import Comment_proccesor as CP 
from Test4.classifier import Classifier


if __name__ == '__main__':
    
    obj = Classifier()
    obj.classify("Que bonito esta esto")
    print obj.get_label()
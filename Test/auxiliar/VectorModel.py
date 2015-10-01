'''
Created on 22/5/2015
@author: Jorge Andoni Valverde Tohalino
@email: andoni.valverde@ucsp.edu.pe
'''

from scipy import spatial
import math
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from Utils import compress , expand

class VectorModel(object):
    
    def __init__(self , data=None):
        self.__data = data
        self.__vectorizer = []
        self.__corpus = []
        self.__transformer = []
        self.__corpus_tf_idf = [] 
    
    def prepare_models(self):
        self.__vectorizer = CountVectorizer()
        vector = self.__vectorizer.fit_transform(self.__data)        
        self.__corpus = vector.toarray()
        self.__transformer = TfidfTransformer()        
        tfidf = self.__transformer.fit_transform(self.__corpus)        
        self.__corpus_tf_idf = tfidf.toarray()        
        self.__compressed = []
        for i in self.__corpus_tf_idf:
            vec = compress(i)            
            self.__compressed.append(vec)
        for i in self.__compressed:
            print i 
        return [self.__vectorizer, self.__transformer, self.__compressed]
    
    def set_models(self, vectorizer, transformer):
        self.__vectorizer = vectorizer
        self.__transformer = transformer
        
    def get_comment_frequency_vector(self, comments):        
        vectores = self.__vectorizer.transform(comments).toarray()
        return vectores 
    
    def get_comment_tf_idf_vector(self, comments):
        vector = self.get_comment_frequency_vector(comments)
        result = self.__transformer.transform(vector).toarray()
        return result

if __name__ == '__main__':
    
    c1 = "vandal arranc nuev lapiz picass"
    c2 = "ojal espan igual rt brasil necesit diplom ejerc period"
    c3 = "vam chilen ultim esfuerz banc qued logr teleton necesit"
    c4 = "buen dias mil graci rt buen dia concejal favorit"
    c5 = "tap leid licenci histori contemporane mast integracion europeav ironi"
    comments = [c1, c2, c3, c4, c5]
    
    obj = VectorModel(comments)
    obj.prepare_models()
    
    res = obj.get_comment_tf_idf_vector(["tap leid" , "buen dias"])
    print res[0]
    vec1 = compress(res[0])
    print vec1
    
    vec =expand(vec1)
    print vec 

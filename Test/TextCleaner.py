#!/usr/bin/env python
# -*- coding: utf-8 -*- 
'''
Created on 15/5/2015
@author: Jorge Andoni Valverde Tohalino
@email: andoni.valverde@ucsp.edu.pe
'''
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')

import re
import unicodedata
from unicodedata import normalize
from split import separar
import snowballstemmer
import string

stopWordFile = 'resource/stopwords_spanish.txt'

class TextCleaner(object):
    
    def __init__(self, comment="" , flag=True):
        self.__comment = comment
        self.__flag = flag
        self.__new_comment = self.process_comment(self.__comment)
    
    def remove_accent(self , word):
        word= word.replace("á", "a")
        word= word.replace("é", "e")
        word= word.replace("í", "i") 
        word= word.replace("ó", "o")
        word= word.replace("ú", "u")
        word= word.replace("à", "a")
        word= word.replace("è", "e")
        word= word.replace("ì", "i") 
        word= word.replace("ó", "o")
        word= word.replace("ú", "u")
        word= word.replace("ä", "a")
        word= word.replace("ë", "e")
        word= word.replace("ï", "i")
        word= word.replace("ö", "o")
        word= word.replace("ü", "u")
        word= word.replace("Á", "a")
        word= word.replace("É", "e")
        word= word.replace("Í", "i") 
        word= word.replace("Ó", "o")
        word= word.replace("Ú", "u")
        word= word.replace("À", "a")
        word= word.replace("È", "e")
        word= word.replace("Ì", "i") 
        word= word.replace("Ò", "o")
        word= word.replace("Ù", "u")
        word= word.replace("Ñ", "N")
        word= word.replace("ñ", "n")
        return word 
    
    def processHashTag(self ,text):
        words = text.split()
        new = ""
        for i in words:
            if i.find('#') != -1:
                i = re.sub(r'#([^\s]+)', r'\1', i)
                i = separar(i)
                new = new + i + " "
            else:
                new = new + i + " "
        return new        

    def find_symbol(self , word):
        alphabet = "abcdefghijklmnñopqrstuvwxyz"
        pos = 0
        flag = 0
        for i in word:
            if alphabet.find(i) != -1:
                pos = pos + 1
            else:
                flag = 1
                break
        return [flag , pos]

    def split_symbols(self ,lista):
        new = []
        for i in lista:
            val = self.find_symbol(i)
            if val[0] == 0:
                new.append(i)
            else:
                pos = val[1]
                if pos == 0:
                    new.append(i)
                else:
                    param = len(i)-pos
                    uno = i[:pos]
                    dos = i[-param:]
                    new.append(uno)
                    new.append(dos)
        return new

    def lemmatizer(self ,word):
        stemmer = snowballstemmer.stemmer('spanish');
        return stemmer.stemWord(word)

    def lemmatized_comment(self , comment):
        lista = comment.split()
        lista = self.split_symbols(lista)
        lematizado = ""
        for i in lista:
            i = self.lemmatizer(i)
            lematizado = lematizado + i + " "
        lematizado = lematizado[:-1]
        return lematizado

    def lemmatized_words(self, comentario):
        lista = comentario.split()
        lematizado = ""
        for i in lista:
            i = self.lemmatizer(i)
            lematizado = lematizado + i + " "
        lematizado = lematizado[:-1]    
        return lematizado

    def remove_stop_word(self, comentario):
        arch = open(stopWordFile , 'r')
        stops = []
        for line in arch:
            word = line.strip()
            stops.append(word)
        text_list = []
        words = re.split("\s+",comentario)        
        for word in words:
            if len(word)>1 and (not word in stops):
                text_list.append(word)
        return " ".join(text_list)
        
    def process_comment(self , comentario):
        comentario = comentario.strip('RT')        
        comentario = self.remove_accent(comentario)        
        comentario = comentario.lower()
        comentario = re.sub('((www\.[\s]+)|(https?://[^\s]+))','',comentario) 
        comentario = re.sub('@[^\s]+','',comentario) 
        comentario = re.sub('[\s]+', ' ', comentario)
        comentario = self.processHashTag(comentario)
        comentario = comentario.strip('\'"')
        signos = ['$' , '1' , '2'  , '3' ,  '4' , '5' , '6' , '7' , '8' , '9' , '0' '¿' , '¡' , ',' , '”' , '“' , '«' , '»']
        
        for c in signos:
            comentario = comentario.replace(c , "")
        
        predicate = lambda x:x not in string.punctuation
        comentario  = filter(predicate, comentario)

                            
        pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
        if self.__flag:
            comentario = self.remove_stop_word(comentario)
        result = pattern.sub(r"\1\1", comentario)
        if len(result) == 0:
            return "None!"
        else:
            comentario = re.sub('\W+',' ', result)
            return self.lemmatized_comment(comentario)            
            #return comentario
                
    def remove_punctuation_marks(self , word):
        """ Elimina los signos de puntuacion de un texto """
        if re.match("^[a-z0-9\xE1\xE9\xED\xF3\xFA\xF1]+$", word):
            return word
        else:
            new_word = ""
            for i in range(len(word)):
                if re.match("[\w\xE1\xE9\xED\xF3\xFA\xF1]", word[i]):
                    new_word += word[i]
            return new_word 

    def get_processed_comment(self):
        return self.__new_comment


if __name__ == '__main__':
    
    comentario = 'La comPUádñoRa no fúnciona #UnAsco'
    obj = TextCleaner(comentario)
    print obj.get_processed_comment()
    
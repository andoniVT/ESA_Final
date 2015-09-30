#!/usr/bin/env python
# -*- coding: utf-8 -*- 
'''
Created on 13/11/2014

@author: ucsp
'''

import re
import unicodedata
from unicodedata import normalize
from Test3.split import separar
import snowballstemmer
from Test3.settings import stop_words
import string
stopWordFile = stop_words

class Comment_proccesor(object):
    def __init__(self, comment="" , flag=False):
        self.__comment = comment
        self.__flag = flag
        self.__new_comment = self.process_comment(self.__comment)
    
    def remove_accent(self , word):
        word= word.replace("á", "a")
        word= word.replace("é", "e")
        word= word.replace("í", "i") 
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
        #comentario = self.remove_accent(comentario)
        comentario = comentario.strip('RT')
        comentario = comentario.lower()
        comentario = re.sub('((www\.[\s]+)|(https?://[^\s]+))','',comentario) 
        comentario = re.sub('@[^\s]+','',comentario) 
        comentario = re.sub('[\s]+', ' ', comentario)
        comentario = self.processHashTag(comentario)
        comentario = comentario.strip('\'"')
        signos = ['$' , '1' , '2'  , '4' , '5' , '6' , '7' , '¿' , '¡' , ',']
        
        for c in signos:
            comentario = comentario.replace(c , "")
        
        
        
        
        pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
        if self.__flag:
            comentario = self.remove_stop_word(comentario)
        result = pattern.sub(r"\1\1", comentario)
        if len(result) == 0:
            return "None!"
        else:
            return self.lemmatized_comment(result)
            #return result 
    
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

    def remove_punctuation(self, comentario):
        signos = ['$' , '1' , '2'  , '4' , '5' , '6' , '7' , '¿' , '¡' , ',']
        for c in signos:
            comentario = comentario.replace(c , "")

        for c in string.punctuation:
            comentario = comentario.replace(c , "")
        return comentario 
    
    def get_processed_comment(self):
        return self.__new_comment


if __name__ == '__main__':
    
    comentarios = ['La comPUtadoRa no funciona #UnAsco' , 'mas unidos que nunca @rossy' , 'horribleeee 123 no me gusta' , 'no vale $ la pena esto !!!']

    for i in comentarios:
        procesador = Comment_proccesor(i , True)
        print procesador.get_processed_comment()
        
    procesador = Comment_proccesor("hola que" , True)
    print procesador.process_comment("fatal")


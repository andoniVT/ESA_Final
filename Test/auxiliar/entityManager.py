#!/usr/bin/env python
# -*- coding: utf-8 -*- 
'''

@author: andoni
Created on 22/03/2015
'''
from Test4.dbConnection import Connection
import re 

vocabulary = 'resource/slangs_peruvian.txt'
vocabulary2 = 'resource/sentiment_words_spanish.txt'

class EManager(object):
    
    def __init__(self):
        self.__con = Connection()
    
    def add_entities(self, entidades):
        #for i in entidades:
        self.__con.add_entity(entidades)
    
    def add_atributte(self, entidad, texto, polaridad, tipo):
        atributo = [texto, polaridad]
        self.__con.add_atributte(entidad, atributo, tipo)

    
    def percent(self, total, value):
        return (100*value)/float(total)
    
    def get_values(self , nombre_entidad):
        valores = self.__con.get_polarity(nombre_entidad)
        total = sum(valores)
        result = []
        if(total!=0):
            result.append(total)        
            for i in valores:
                value = self.percent(total, i)
                result.append(value)
        return result 
                 

    def polarity_rule(self, value):
        if value>0: return "positivo"
        if value<0: return "negativo"
        if value==0: return "neutral"
    
        



if __name__ == '__main__':
    
    e = EManager()
    #print e.percent(89, 16)
    print e.get_values("Barza")
    #print e.load_value("misio")
    
    
        
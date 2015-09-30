#!/usr/bin/env python
# -*- coding: utf-8 -*- 
'''
Created on 15/11/2014

@author: andoni
'''

import Test3.settings as settings 

class Term(object):
    
    def __init__(self, original_term):
        self.__original_term = original_term
        self.__new_term = original_term
        self.__term_type = settings.TERM_TYPE_NEUTRO
        self.__original_weight = 0
        self.__has_reapeted_letters = False
        self.__has_capital_letters = False
        self.__aditional_weight = list()
        self.__create_new_term()
    
    def __create_new_term(self):
        self.__go_capital_letters()
        self.__go_repeated_letters()
       
    def __go_capital_letters(self):
        if self.__original_term.isupper():
            self.__has_capital_letters = True
        self.__new_term = self.__new_term.lower()
        
    def __go_repeated_letters(self):
        threshold = 2
        size = len(self.__new_term)
        i = 0
        new_word = ""
        while i < size:
            repeated = 0
            new_word += self.__new_term[i]
            while(i < size-1 and self.__new_term[i] == self.__new_term[i+1]):
                i += 1
                repeated += 1
            if repeated > 0:
                new_word += self.__new_term[i]
            if repeated >= threshold:
                self.__has_reapeted_letters = True
            i += 1
        self.__new_term = new_word
    
    def get_original_term(self):
        return self.__original_term
    
    def get_new_term(self):
        return self.__new_term
    
    def get_original_weight(self):
        return self.__original_weight
    
    def get_total_weight(self):
        total = self.__original_weight
        for tmp in self.__aditional_weight:
            total += tmp.get_weight()
        return total
    
    def get_term_type(self):
        return self.__term_type
    
    def has_reapeted_letters(self):
        return self.__has_reapeted_letters
    
    def has_capital_letters(self):
        return self.__has_capital_letters
    
    def get_aditional_weight(self):
        return self.__aditional_weight
    
    def set_term_type(self, term_type):
        self.__term_type = term_type
    
    def set_new_term(self, new_term):
        self.__new_term = new_term
        
    def set_original_weight(self, original_weight):
        self.__original_weight = original_weight
        
    def set_aditional_weight(self, weight, description):
        if(self.__original_weight < 0):
            weight = -weight
        obj_weight = Weight(weight, description) 
        self.__aditional_weight.append(obj_weight)

class Weight(object):
    W_REPEATED_LETTTER = 1
    D_REPEATED_LETTTER = 'let.Rep'
    W_CAPITAL_LETTTER = 1
    D_CAPITAL_LETTTER = 'let.May'
    
    def __init__(self, weight, description):
        self.__weight = weight
        self.__description = description
    
    def get_weight(self):
        return self.__weight
    
    def get_description(self):
        return self.__description


  
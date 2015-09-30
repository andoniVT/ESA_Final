#!/usr/bin/env python
# -*- coding: utf-8 -*- 
'''
Created on 15/11/2014

@author: andoni
'''

from Test3.parameter_text import ParameterText

class Classifier(object):
    ''' Clase encargada de clasificar un comentario como positivo, negativo o neutro '''
    
    def __init__(self):
        self.__obj_parameter = ParameterText()
        self.__contribution_positive = 0
        self.__contribution_negative = 0
        self.__number_elements_positive = 0
        self.__number_elements_negative = 0
        self.__result = 0
        self.__label = ''        
    
    def classify(self, comment, type_option='1'):
        ''' Clasifica un comentario de acuerdo a la opcion elegida'''
        opt = Option()
        self.__obj_parameter.evaluate(comment)
        self.__contribution_positive = self.__obj_parameter.get_contribution_positive()     
        self.__contribution_negative = self.__obj_parameter.get_contribution_negative()
        # Eliminamos la data pasada
        self.__obj_parameter.clean_data()
        self.__result = self.calculate_value(self.__contribution_positive, self.__contribution_negative)
        if type_option == '1': self.__label = opt.option1(self.__result)
        elif type_option == '2': self.__label = opt.option2(self.__result)
        elif type_option == '3': self.__label = opt.option3(self.__result)
        else: self.__label = opt.option4(self.__result)
        #print self.__label
    
    def get_contribution_positive(self):
        return self.__contribution_positive
    
    def get_contribution_negative(self):
        return self.__contribution_negative
    
    def get_score(self):
        return self.__result
    
    def get_label(self):
        return self.__label
                   
    def calculate_value(self, positive, negative):
        ''' Calcula el score'''
        dif = positive + negative
        summ = positive - negative
        if summ == 0: return 0
        result = 0.0
        result = dif/float(summ)
        return result

class Option:
    POSITIVE = 'P'
    NEGATIVE = 'N'
    NEUTRAL = 'NEU'
    UNDEFINED = 'no definido'
    NON_POSITIVE = 'no positivo'
    NON_NEGATIVE = 'no negativo'
    
    def option1(self, value):
        if value > 0.05: return self.POSITIVE
        elif value < -0.05: return self.NEGATIVE
        else: return self.NEUTRAL
        
    def option2(self, value):
        if value > 0.02: return self.POSITIVE
        elif value < -0.04: return self.NEGATIVE
        else: return self.UNDEFINED
        
    def option3(self, value):
        if value > 0: return self.POSITIVE
        else: return self.NON_POSITIVE
        
    def option4(self, value):
        if value < 0: return self.NEGATIVE
        else: return self.NON_NEGATIVE
        

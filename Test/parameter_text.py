#!/usr/bin/env python
# -*- coding: utf-8 -*- 
'''
Created on 15/11/2014

@author: andoni
'''

import re 
import Test3.settings as settings
import Test3.corpus as corpus
from Test3.term import Term
from Test3.manager_rule import Manager , Pattern
import Test3.commentPreprocessor as CP 

class ParameterText(object):
    def __init__(self):
        '''
        Constructor
        '''
        self.__comment = ""
        self.__contribution_positive = 0
        self.__contribution_negative = 0
        self.__number_elements_positive = 0
        self.__number_elements_negative = 0
        self.__crude_term_list = list()
        self.__term_list = list()
        self.__pattern_list = list()
        self.__contribution_words_pos = list()
        self.__contribution_words_neg = list()
        self.__contribution_emoticons_pos = list()
        self.__contribution_emoticons_neg = list()
        self.__contribution_combinations_pos = list()
        self.__contribution_combinations_neg = list()        
        self.__emoticons = corpus.emoticons_list(settings.EMOTICONS)
        self.__booster_words = corpus.booster_words_list(settings.BOOSTER_WORDS_SPANISH)
        self.__negating_words = corpus.negating_words_list(settings.NEGATING_WORDS_SPANISH)
        self.__punctuation = corpus.punctuation_list(settings.PUNCTUATION)        
        self.__stopwords_list = corpus.stopwords_list(settings.STOPWORDS_SPANISH_OPINION_MINING)
        self.__words_and_slangs = corpus.words_and_slangs_list(settings.SENTIMENT_WORDS_SPANISH, settings.SLANGS_PERUVIAN)        
        self.__combinations = corpus.combinations_list(settings.COMBINATIONS_SPANISH, settings.COMBINATIONS_SLANGS_PERUVIAN)

    def evaluate(self, comment):        
        proccess = CP.Comment_proccesor(comment , False)
        comment = proccess.get_processed_comment()
        self.__comment = comment
        comment = self.__search_combinations(comment)
        self.__init_term_list(comment)
        for term in self.__crude_term_list:
            self.__tagging(term)
        self.__apply_rules()
        self.__analize_contributions()

    
    def __tagging(self, term):
        obj_term = Term(term)
        new_term = obj_term.get_new_term()
        # tipo = emoticon
        result = self.__search(self.__emoticons, term)
        if result != settings.TERM_NOT_FOUND:
            obj_term.set_term_type(settings.TERM_TYPE_EMOTICON)
            obj_term.set_original_weight(int(self.__emoticons[result]))
            self.__term_list.append(obj_term)
            return

        # tipo = puntuacion
        result = self.__search(self.__punctuation, new_term)
        if result != settings.TERM_NOT_FOUND:
            obj_term.set_term_type(settings.TERM_TYPE_PUNCTUATION)
            obj_term.set_original_weight(int(self.__punctuation[result]))
            self.__term_list.append(obj_term)
            return

        # tipo = palabras de realce
        result = self.__search(self.__booster_words, new_term)
        if result != settings.TERM_NOT_FOUND:
            obj_term.set_term_type(settings.TERM_TYPE_BOOSTER)
            obj_term.set_original_weight(int(self.__booster_words[result]))
            self.__term_list.append(obj_term)
            return

        # tipo = negacion
        if new_term in self.__negating_words:
            obj_term.set_term_type(settings.TERM_TYPE_NEGATING)
            self.__term_list.append(obj_term)
            return

        # tipo = palabra o jerga
        #new_term = self.__corrector.correct(new_term)
        #obj_term.set_new_term(new_term)
        #new_dictionary = dict(self.__words_and_slangs.items() + self.__new_simple_vocabulary.items() + self.__modified_words.items())        
        result = self.__search(self.__words_and_slangs, new_term)
        #result = self.__search(new_dictionary, new_term)
        if result != settings.TERM_NOT_FOUND:
            obj_term.set_term_type(settings.TERM_TYPE_WORD_SLANG)
            obj_term.set_original_weight(int(self.__words_and_slangs[result]))
            #obj_term.set_original_weight(int(new_dictionary[result]))
            self.__term_list.append(obj_term)
            return

        # tipo = neutral
        obj_term.set_term_type(settings.TERM_TYPE_NEUTRO)
        self.__term_list.append(obj_term)
                      
    def __apply_rules(self):
        manager = Manager(self.__term_list)
        manager.apply_rules()
        self.__pattern_list = manager.get_patterns_list()
    
    def __analize_contributions(self):
        for pattern in self.__pattern_list:
            if pattern.get_contribution_type() == Pattern.CONTRIBUTION_WORD:
                if pattern.get_total_weight() >= 0: self.__contribution_words_pos.append(pattern)
                else: self.__contribution_words_neg.append(pattern)
            elif pattern.get_contribution_type() == Pattern.CONTRIBUTION_EMOTICON:
                if pattern.get_total_weight() >= 0: self.__contribution_emoticons_pos.append(pattern)
                else: self.__contribution_emoticons_neg.append(pattern)
            else:
                if pattern.get_total_weight() >= 0: self.__contribution_combinations_pos.append(pattern)
                else: self.__contribution_combinations_neg.append(pattern)
    
    def get_contribution_words_pos(self):
        total = 0
        for pattern in self.__contribution_words_pos:
            total += pattern.get_total_weight()
        return total
    
    def get_contribution_words_neg(self):
        total = 0
        for pattern in self.__contribution_words_neg:
            total += pattern.get_total_weight()
        return total
    
    def get_contribution_emoticons_pos(self):
        total = 0
        for pattern in self.__contribution_emoticons_pos:
            total += pattern.get_total_weight()
        return total
    
    def get_contribution_emoticons_neg(self):
        total = 0
        for pattern in self.__contribution_emoticons_neg:
            total += pattern.get_total_weight()
        return total
    
    def get_contribution_combinations_pos(self):
        total = 0
        for pattern in self.__contribution_combinations_pos:
            total += pattern.get_total_weight()
        return total
    
    def get_contribution_combinations_neg(self):
        total = 0
        for pattern in self.__contribution_combinations_neg:
            total += pattern.get_total_weight()
        return total
    
    def get_contribution_positive(self):
        self.__contribution_positive = self.get_contribution_words_pos() + self.get_contribution_emoticons_pos() + self.get_contribution_combinations_pos()     
        return self.__contribution_positive  
    
    def get_contribution_negative(self):
        self.__contribution_negative = self.get_contribution_words_neg() + self.get_contribution_emoticons_neg() + self.get_contribution_combinations_neg()
        return self.__contribution_negative 
    
    def get_number_words_pos(self):
        return len(self.__contribution_words_pos)
    
    def get_number_words_neg(self):
        return len(self.__contribution_words_neg)
    
    def get_number_emoticons_pos(self):
        return len(self.__contribution_emoticons_pos)
    
    def get_number_emoticons_neg(self):
        return len(self.__contribution_emoticons_neg)   
    
    def get_number_combinations_pos(self):
        return len(self.__contribution_combinations_pos)
    
    def get_number_combinations_neg(self):
        return len(self.__contribution_combinations_neg)
    
    def get_number_elements_positive(self):
        self.__number_elements_positive = self.get_number_words_pos() + self.get_number_emoticons_pos() + self.get_number_combinations_pos()     
        return self.__number_elements_positive  
    
    def get_number_elements_negative(self):
        self.__number_elements_negative = self.get_number_words_neg() + self.get_number_emoticons_neg() + self.get_number_combinations_neg()
        return self.__number_elements_negative    
   
    def __init_term_list(self, comment):
        tmp_list = re.split("\s+",comment) # Divide el texto por cualquier caracter en blanco
        for term in tmp_list:
            if not term in self.__stopwords_list:
                if term in self.__emoticons:
                    self.__crude_term_list.append(term)
                else:
                    process = CP.Comment_proccesor()
                    term = process.remove_punctuation_marks(term)                    
                    if len(term) > 0:
                        index = term.find("!")
                        if index == -1: index = term.find("?")
                        if index > 0:
                            self.__crude_term_list.append(term[:index])
                            self.__crude_term_list.append(term[index:])
                        else:
                            self.__crude_term_list.append(term)
                   
    def __search (self, tmp_list, term):
        for word in tmp_list:
            if word.count(settings.FLEXIS_SIMBOL) > 0: # Si contiene flexis
                root_word = word.replace(settings.FLEXIS_SIMBOL, "")
                if term.startswith(root_word, 0) and len(term) > len(root_word):
                    return word
            else:
                if term == word:
                    return word
        return settings.TERM_NOT_FOUND
    
    def __search_combinations(self, comment):
        comment_lower = comment.lower()
        #new_dictionary = dict(self.__combinations.items() + self.__new_combination_vocabulary.items() + self.__modified_combinations.items())        
        #for combination in new_dictionary:            
        for combination in self.__combinations:            
            if comment_lower.find(combination) >= 0:
                obj_term = Term(combination)
                obj_term.set_term_type(settings.TERM_TYPE_COMBINATION)
                obj_term.set_original_weight(int(self.__combinations[combination]))
                self.__term_list.append(obj_term)
                comment = re.sub(combination, "", comment, flags=re.IGNORECASE)
        return comment
    
    def print_terms(self):
        for pattern in self.__pattern_list:
            print(pattern.get_contribution_type(), pattern.description(), pattern.get_total_weight())
            
    def clean_data(self):
        ''' Re-inicializa todas las listas '''
        self.__crude_term_list = list()
        self.__term_list = list()
        self.__pattern_list = list()
        self.__contribution_words_pos = list()
        self.__contribution_words_neg = list()
        self.__contribution_emoticons_pos = list()
        self.__contribution_emoticons_neg = list()
        self.__contribution_combinations_pos = list()
        self.__contribution_combinations_neg = list()
            
if __name__ == '__main__':
    import time
    print("Starting... ",time.strftime("%H:%M:%S %d %b"))

    obj = ParameterText()
    comment = "poco bueno muy bueno poco malo muy malo" 
    #comment = "muy bueno!!! muy mal!!! poco bueno!!! poco mal!!!" 
    #comment = "no muy bueno no muy malo"
    #comment = "@ClaroPeru Hola, actualmente tengo un Nextel pero quiero migrar a Claro manteniendo el mismo número. Cuál es el procedimiento?"
    obj.evaluate(comment)
    obj.print_terms()
    print("Finished... ",time.strftime("%H:%M:%S %d %b"))  
     

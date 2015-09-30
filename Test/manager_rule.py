#!/usr/bin/env python
# -*- coding: utf-8 -*- 
'''
Created on 15/11/2014

@author: andoni
'''

import Test3.settings as settings

class Manager(object):
    '''
    classdocs
    '''
    def __init__(self, term_list):
        self.__term_list = term_list
        self.__pattern_list = list()
        self.__size = len(self.__term_list)
        
    def get_patterns_list(self):
        return self.__pattern_list 
       
    def apply_rules(self):
        i = 0
        while i < self.__size:
            i = self.__next_position(i)
            
    def __next_position(self, i):
        if self.__term_list[i].get_term_type() == settings.TERM_TYPE_WORD_SLANG:
            return self.__analize_word_slang(i)
        if self.__term_list[i].get_term_type() == settings.TERM_TYPE_COMBINATION:
            return self.__analize_combinations(i)
        if self.__term_list[i].get_term_type() == settings.TERM_TYPE_EMOTICON:
            return self.__analize_emoticons(i)
        if self.__term_list[i].get_term_type() == settings.TERM_TYPE_NEGATING:
            return self.__analize_negating_words(i)
        if self.__term_list[i].get_term_type() == settings.TERM_TYPE_BOOSTER:
            return self.__analize_booster_words(i)
        else:
            return i+1
         
    def __analize_word_slang(self, i):
        pattern = Pattern()
        pattern.add_term(self.__term_list[i])
        pattern.set_contribution_type(Pattern.CONTRIBUTION_WORD)
        if i <= self.__size-2:
            if self.__term_list[i+1].get_term_type() == settings.TERM_TYPE_PUNCTUATION:
                pattern.add_term(self.__term_list[i+1])
                pattern.set_rule(Pattern.RULE8)
                pattern.identify_weight() 
                self.__pattern_list.append(pattern)
                return i+2
        pattern.set_rule(Pattern.RULE1)
        pattern.identify_weight()             
        self.__pattern_list.append(pattern)
        return i+1
    
    def __analize_combinations(self, i):
        pattern = Pattern()
        pattern.add_term(self.__term_list[i])
        pattern.set_contribution_type(Pattern.CONTRIBUTION_COMBINATION)
        pattern.set_rule(Pattern.RULE2)
        pattern.identify_weight()             
        self.__pattern_list.append(pattern)
        return i+1
    
    def __analize_emoticons(self, i):
        pattern = Pattern()
        pattern.add_term(self.__term_list[i])
        pattern.set_contribution_type(Pattern.CONTRIBUTION_EMOTICON)
        pattern.set_rule(Pattern.RULE3)
        pattern.identify_weight()            
        self.__pattern_list.append(pattern)
        return i+1
    
    def __analize_negating_words(self, i):
        if i <= self.__size-3:
            if self.__term_list[i+1].get_term_type() == settings.TERM_TYPE_BOOSTER and self.__term_list[i+2].get_term_type() == settings.TERM_TYPE_WORD_SLANG:
                pattern = Pattern()
                pattern.add_term(self.__term_list[i])
                pattern.add_term(self.__term_list[i+1])
                pattern.add_term(self.__term_list[i+2])
                pattern.set_contribution_type(Pattern.CONTRIBUTION_WORD)
                pattern.set_rule(Pattern.RULE5)
                pattern.identify_weight()            
                self.__pattern_list.append(pattern)
                return i+3
            if self.__term_list[i+1].get_term_type() == settings.TERM_TYPE_WORD_SLANG and self.__term_list[i+2].get_term_type() == settings.TERM_TYPE_BOOSTER:
                pattern = Pattern()
                pattern.add_term(self.__term_list[i])
                pattern.add_term(self.__term_list[i+1])
                pattern.add_term(self.__term_list[i+2])
                pattern.set_contribution_type(Pattern.CONTRIBUTION_WORD)
                pattern.set_rule(Pattern.RULE51)
                pattern.identify_weight()            
                self.__pattern_list.append(pattern)
                return i+3
        if i <= self.__size-2:
            if self.__term_list[i+1].get_term_type() == settings.TERM_TYPE_WORD_SLANG:
                pattern = Pattern()
                pattern.add_term(self.__term_list[i])
                pattern.add_term(self.__term_list[i+1])
                pattern.set_contribution_type(Pattern.CONTRIBUTION_WORD)
                pattern.set_rule(Pattern.RULE4)  
                pattern.identify_weight()           
                self.__pattern_list.append(pattern)
                return i+2     
        return i +1
           
    def __analize_booster_words(self, i):
        if i <= self.__size-3:
            if self.__term_list[i+1].get_term_type() == settings.TERM_TYPE_WORD_SLANG and self.__term_list[i+2].get_term_type() == settings.TERM_TYPE_PUNCTUATION:
                pattern = Pattern()
                pattern.add_term(self.__term_list[i])
                pattern.add_term(self.__term_list[i+1])
                pattern.add_term(self.__term_list[i+2])
                pattern.set_contribution_type(Pattern.CONTRIBUTION_WORD)
                pattern.set_rule(Pattern.RULE7)
                pattern.identify_weight()            
                self.__pattern_list.append(pattern)
                return i+3
        if i <= self.__size-2:
            if self.__term_list[i+1].get_term_type() == settings.TERM_TYPE_WORD_SLANG:
                pattern = Pattern()
                pattern.add_term(self.__term_list[i])
                pattern.add_term(self.__term_list[i+1])
                pattern.set_contribution_type(Pattern.CONTRIBUTION_WORD)
                pattern.set_rule(Pattern.RULE6)
                pattern.identify_weight()            
                self.__pattern_list.append(pattern)
                return i+2
        return i +1
    

class Pattern(object):
    CONTRIBUTION_EMOTICON = "EMOTICON"
    CONTRIBUTION_WORD = 'WORD'
    CONTRIBUTION_COMBINATION = "COMBINATION"
    
    RULE1 = settings.TERM_TYPE_WORD_SLANG
    RULE2 = settings.TERM_TYPE_COMBINATION
    RULE3 = settings.TERM_TYPE_EMOTICON
    RULE4 = settings.TERM_TYPE_NEGATING + settings.TERM_TYPE_WORD_SLANG
    RULE5 = settings.TERM_TYPE_NEGATING + settings.TERM_TYPE_BOOSTER + settings.TERM_TYPE_WORD_SLANG
    RULE51 = settings.TERM_TYPE_NEGATING + settings.TERM_TYPE_WORD_SLANG + settings.TERM_TYPE_BOOSTER
    RULE6 = settings.TERM_TYPE_BOOSTER + settings.TERM_TYPE_WORD_SLANG
    RULE7 = settings.TERM_TYPE_BOOSTER + settings.TERM_TYPE_WORD_SLANG + settings.TERM_TYPE_PUNCTUATION
    RULE8 = settings.TERM_TYPE_WORD_SLANG + settings.TERM_TYPE_PUNCTUATION
        
    def __init__(self):
        self.__total_weight = 0
        self.__type = self.CONTRIBUTION_WORD
        self.__term_list = list()
        self.__rule = ""
        
    def add_term(self, term):
        self.__term_list.append(term)
           
    def set_contribution_type(self, contribution_type):
        self.__type = contribution_type
        
    def set_rule(self, rule):
        self.__rule = rule
    
    def get_contribution_type(self):
        return self.__type
    
    def get_total_weight(self):
        return self.__total_weight
    
    def identify_weight(self):     
        if self.__rule == self.RULE1:# pesimo
            self.__total_weight = self.__term_list[0].get_total_weight()
            return
        elif self.__rule == self.RULE2:# nada de nada 
            self.__total_weight = self.__term_list[0].get_total_weight()
            return
        elif self.__rule == self.RULE3:# :)
            self.__total_weight = self.__term_list[0].get_total_weight()
            return
        elif self.__rule == self.RULE4:# no es bueno
            self.__total_weight = -self.__term_list[1].get_total_weight()
            return
        elif self.__rule == self.RULE5:# no es muy bueno
            w1 = self.__term_list[1].get_total_weight()
            w2 = self.__term_list[2].get_total_weight()
            i = 1
            tmp = w1
            if w1 > 0 and w2 < 0: tmp = -w1
            if w1 < 0 and w2 < 0: tmp = -w1
            if w2 < 0: i = -i           
            self.__total_weight = -(tmp + w2) + i
            return
        elif self.__rule == self.RULE51:# no gusta mucho
            w1 = self.__term_list[1].get_total_weight()
            w2 = self.__term_list[2].get_total_weight()
            i = 1
            tmp = w2
            if w2 > 0 and w1 < 0: tmp = -w2
            if w2 < 0 and w1 < 0: tmp = -w2
            if w1 < 0: i = -i           
            self.__total_weight = -(w1 + tmp) + i
            return  
        elif self.__rule == self.RULE6:# muy bueno
            w1 = self.__term_list[0].get_total_weight()
            w2 = self.__term_list[1].get_total_weight()
            tmp = w1
            if  w1 > 0 and w2 < 0: tmp = -w1
            if  w1 < 0 and w2 < 0: tmp = -w1
            self.__total_weight = tmp + w2
            return
        elif self.__rule == self.RULE7:# muy bueno!!!
            w1 = self.__term_list[0].get_total_weight()
            w2 = self.__term_list[1].get_total_weight()
            w3 = self.__term_list[2].get_total_weight()
            if  w1 > 0 and w2 < 0: 
                w1 = -w1 
                w3 = -w3
            if  w1 < 0 and w2 > 0: 
                w1 = -w1 
                w3 = -w3
            self.__total_weight = w1 + w2 + w3
            return
        elif self.__rule == self.RULE8:#pesimo!!!
            w1 = self.__term_list[0].get_total_weight()
            w2 = self.__term_list[1].get_total_weight()
            if  w1 < 0: w2 = -1*w2
            self.__total_weight = w1 + w2
            return
        else:
            des = ""
            for term in self.__term_list:
                des += " "+term.get_new_term()
            self.__total_weight = self.__term_list[0].get_total_weight()
            return 
    
    def description(self):
        des = ""
        for term in self.__term_list:
            des += " "+term.get_original_term()
        return des

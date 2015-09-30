#!/usr/bin/env python
# -*- coding: utf-8 -*- 
'''
Created on 15/11/2014

@author: andoni
'''

import Test3.settings as settings
import re 

def stopwords_list(file_path):
    return __read_files_1columm(file_path)

def stemm_list(file_path):
    return __read_files_2columms(file_path)

def emoticons_list(file_path):
    return __read_files_2columms(file_path, settings.SPLITTER_WEIGHTS)

def sentiment_words_list(file_path):
    return __read_files_2columms(file_path, settings.SPLITTER_WEIGHTS)

def booster_words_list(file_path):
    return __read_files_2columms(file_path, settings.SPLITTER_WEIGHTS)

def slang_words_list(file_path):
    return __read_files_2columms(file_path, settings.SPLITTER_WEIGHTS)

def negating_words_list(file_path):
    return __read_files_1columm(file_path)

def punctuation_list(file_path):
    return __read_files_2columms(file_path, settings.SPLITTER_WEIGHTS)

def new_words_list(file_path):
    return __read_files_2columms(file_path, settings.SPLITTER_WEIGHTS)


def words_and_slangs_list(file_path1, file_path2):
    list1 = __read_files_2columms(file_path1, settings.SPLITTER_WEIGHTS)
    list2 = __read_files_2columms(file_path2, settings.SPLITTER_WEIGHTS)
    result = {}
    result.update(list1)
    result.update(list2)
    return result

def combinations_list(file_path1, file_path2):
    list1 = __read_files_2columms(file_path1, settings.SPLITTER_WEIGHTS)
    list2 = __read_files_2columms(file_path2, settings.SPLITTER_WEIGHTS)
    result = {}
    result.update(list1)
    result.update(list2)
    return result

def __read_files_2columms(file_path, splitter=" "):
    my_list = dict()
    #file = open(file_path, 'r', encoding=settings.ENCODING)
    file = open(file_path, 'r')
    while True:
        line = file.readline()
        if not line: break
        tmp = re.split(splitter, line)
        my_list[replace_tilde(tmp[0].strip())] = tmp[1].strip()
    file.close()    
    return my_list  


def __read_files_1columm(file_path):
    my_list = dict()
    #file = open(file_path, 'r', encoding=settings.ENCODING)
    file = open(file_path, 'r')
    while True:
        line = file.readline()
        if not line: break
        my_list[replace_tilde(line.strip())] = 0
    file.close()
    return my_list 

def replace_tilde(word):
    word= word.replace("\xE1", "a")
    word= word.replace("\xE9", "e")
    word= word.replace("\xED", "i")
    word= word.replace("\xF3", "o")
    word= word.replace("\xFA", "u")
    return word 



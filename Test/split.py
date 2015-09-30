#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 26/10/2014

@author: Andoni Valverde Tohalino
@email: andoni.valverde@ucsp.edu.pe
'''
import re
from itertools import groupby
from Test3.settings import big_text
def viterbi_segment(text):
    probs, lasts = [1.0], [0]
    for i in range(1, len(text) + 1):
        prob_k, k = max((probs[j] * word_prob(text[j:i]), j)
                        for j in range(max(0, i - max_word_length), i))
        probs.append(prob_k)
        lasts.append(k)
    words = []
    i = len(text)
    while 0 < i:
        words.append(text[lasts[i]:i])
        i = lasts[i]
    words.reverse()
    return words, probs[-1]

def word_prob(word): return dictionary.get(word, 0) / total
def words(text): return re.findall('[a-z]+', text.lower()) 
dictionary = dict((w, len(list(ws)))
                  for w, ws in groupby(sorted(words(open(big_text).read()))))
max_word_length = max(map(len, dictionary))
total = float(sum(dictionary.values()))

def separar(word):
    return ' '.join(viterbi_segment(word)[0])



if __name__ == '__main__':
    
    print separar("holamundo")
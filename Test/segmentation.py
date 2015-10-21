#!/usr/bin/env python
# -*- coding: utf-8 -*- 
'''
Created on 18/3/2015

@author: ucsp
'''
from nltk import tokenize
import itertools
import re
import nltk.tokenize.punkt
import pickle
import codecs

class Segmentation(object):
    
    def __init__(self , sentence):
        self.abbreviations = {'dr.': 'doctor', 'sr.': 'senior',  'sra.': 'seniora', 'srta.': 'seniorita', 'vs.': 'versus'}
        self.terminators = ['.', '!', '?' , ',' , ';' ,'pero' , 'sin embargo' , 'no obstante', 'por el contrario' ,
                               'en cambio' , 'con todo' , 'de todas maneras' , 'aunque', 'tampoco' ,
                                'porque' , 'por esta razon', 'por consiguiente' ,'asi pues' , 'de ahi que', 
                                'asi que', 'de modo que', 'es decir'  , 'o sea', 'esto es', 'mejor dicho', 
                                'por ejemplo'  ]
        self.wrappers = ['"', "'", ')', ']', '}']
        self.sentence = sentence
    
    def find_all(self, a_str, sub):
        start = 0
        while True:
            start = a_str.find(sub, start)
            if start == -1:
                return
            yield start
            start += len(sub)
    
    def find_sentence_end(self ,paragraph):
        [possible_endings, contraction_locations] = [[], []]
        contractions = self.abbreviations.keys()
        sentence_terminators = self.terminators + [terminator + wrapper for wrapper in self.wrappers for terminator in self.terminators]
        for sentence_terminator in sentence_terminators:
            t_indices = list(self.find_all(paragraph, sentence_terminator))
            possible_endings.extend(([] if not len(t_indices) else [[i, len(sentence_terminator)] for i in t_indices]))
        for contraction in contractions:
            c_indices = list(self.find_all(paragraph, contraction))
            contraction_locations.extend(([] if not len(c_indices) else [i + len(contraction) for i in c_indices]))
        possible_endings = [pe for pe in possible_endings if pe[0] + pe[1] not in contraction_locations]
        if len(paragraph) in [pe[0] + pe[1] for pe in possible_endings]:
            max_end_start = max([pe[0] for pe in possible_endings])
            possible_endings = [pe for pe in possible_endings if pe[0] != max_end_start]
        possible_endings = [pe[0] + pe[1] for pe in possible_endings if sum(pe) > len(paragraph) or (sum(pe) < len(paragraph) and paragraph[sum(pe)] == ' ')]
        end = (-1 if not len(possible_endings) else max(possible_endings))
        return end 
    
    def find_sentences(self):
        end = True
        sentences = []
        while end > -1:
            end = self.find_sentence_end(self.sentence)
            if end > -1:
                sentences.append(self.sentence[end:].strip())
                self.sentence = self.sentence[:end]
        sentences.append(self.sentence)
        sentences.reverse()
        return sentences



filename = "testTrain.txt"
filename2 = "segmenterTrain.pk"


class Segmentation2(object):
    
    def __init__(self):        
        self.__text_segment_train = filename 
        self.__train_segment = filename2
    
    
    def train_punkt(self):
        tokenizer = nltk.tokenize.punkt.PunktSentenceTokenizer()
        text = codecs.open(self.__text_segment_train, "r", "utf8").read()
        tokenizer.train(text)
        out = open(self.__train_segment , "wb")
        pickle.dump(tokenizer, out)
        out.close()
    
    def segment_text(self, text):
        #file2 = open("testTrain.pk", 'r')
        file2 = open(self.__train_segment, 'r')
        segmenter = pickle.Unpickler(file2).load()
        segments = segmenter.tokenize(text)
        return segments     
        
if __name__ == '__main__':
    
    obj = Segmentation2()
    #obj.train_punkt()
    print obj.segment_text("Yo no he comentado el partido. pero HALA MADRID")
    print obj.segment_text("Felicitaciones al Real Madrid. en las buenas y en las malas. Visca Barza!")
    
    
    
    
    
    '''
    
    #seg = Segmentation("Felicitaciones al Real Madrid, en las buenas y en las malas Visca Barza!")
    text_ = "Felicitaciones al Real Madrid, en las buenas y en las malas Visca Barza!"
    text = "El mejor del F.C Barcelona en la final en mi opinión fue Pinto, el mejor del Real Madrid aunque no marcó fue Benzema, tiene mucha calidad."
    text2 = "Tranquilos, messi se esta dosificando para el mundial... Que tiembre brasil!!"
    text3 = "Mi casa, mi familia, mi novia y mi Madrid ganando la copa al barsa...no se puede pedir nada más. #HalaMadrid"
    text4 = "Donde están los que decían que Gareth Bale no valía cien millones? Jaja Habladores! HALA MADRID"
    text5 = "Yo no he comentado el partido pero HALA MADRID"
    text6 = "Si no os digo cada vez que habla Ramos lo mucho que me encanta su voz y su acento tampoco me quedo tranquila"
    text7 = "Alves echate unos bailes con neymar para celebrar la copa del rey , del MADRID !! #HalaMadrid !"
    text8 = "Una lectura positiva de todo esto, los señores Messi y Neymar ya podéis pensar en el mundial de los cojones. Id tranquilos chicos"
    text9 = "Sergio Ramos subiendo a recoger la copa con la bandera del Betis pa tocar los cojones"
    text10 = "Real como no quererte si siempre demuestras quien eres en la chanca?"
    text11 = "Tanto Messi y Neymar y al final el Madrid sin Cristiano gana la copa"
    text12 = "Su salvador supremo Messi no pateo ni una lata en ese partido, la burla"
    text13 = "Si le dan la copa a Cristiano lloro de seguro"
    text14 = "Y por último, grandísima noticia la vuelta del Bale de la Premier, a los espacios y sin Cristiano, él gana partidos. Mucho mejor que Neymar"
    text15 = "Me da rabia que el real madrid haya ganado, pero es lo qie hay"
    text16 = "Como juega mi Madrid como se quedan los catalanes HALA MADRID"
    text17 = "Palabras de Sergios Ramos; Ostias Picha que puedo reventar otra copa pal piso jajajaja"
    text18 = "espectacular el Madrid y Gareth Bale.  2-1 y para casa los del Barça jajaja"
    text19 = "Cuantaaaa felicidad! despues de una tarde perfecta ;), el madrid ganaaa la copa del rey al barca!"
    text20 = "El Barça tiene que hacer muchos cambios, empezando por la directiva"
    text21 ="Se despide a un Barça de época que termina un legado jugando a lo mismo. El fútbol, para ser competitivo, debe renovar estilos."
    text22 = "Que supremacía la de Bale se los dije, EL PRÍNCIPE GALES BALE, haciendo añicos al Barca."
    text23 ="Los q hoy están Jodidos con el Barça, recuerden q estos saldrán hoy de fiesta y les importa una mierda empezando por Alves y por Neymar"
    text24 = "Me voy a cenar. Enhorabuena a los aficionados merengues. Lo del Barça es para hacérselo mirar,en una semana temporada en blanco. PATÉTICO!"
    text25 = "buen partido de los mandriles. ahora si, me da pena que el reportero de tve no busque la entrevista con bale #nohablamosingles"
    text26 = "Los del barcelona estan alterados no se , puras excusas"
    text27 = "Lo mataría al relator, a los del Real y mas a Cristiano! Ah, y a los ""simpatizantes"" del Real"
    text28 = "El Tata Martino se gana solito la destitucion, Alexis y Pedro estan muchisimo mejores que Neymar, pero la plata es la que juega"
    text29 = "Triunfo merecido, messi desaparecido, Pinto fatal un equipo de primer nivel se merece un portero al menos de garantias y que tenga reflejos"
    text30 = "El Barcelona gana un titulo y es una temporada mediocre, el Madrid gana una copa y es un temporadon!!"
    
    
    seg = Segmentation(text30)
    
    segmentos = seg.find_sentences()
    for i in segmentos:
        print i
    ''' 
    

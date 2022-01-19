# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 19:29:05 2022

@author: emreb
"""

import sqlite_functions as sql
from typing import List
from jpype import JClass, JString, getDefaultJVMPath, shutdownJVM, startJVM, java
import distance_algorithm as dist
import jpype
ZEMBEREK_PATH = r'C:\Users\emreb\Desktop\main_proje\zemberek-full.jar'


if not jpype.isJVMStarted():
    startJVM(getDefaultJVMPath(), '-ea', '-Djava.class.path=%s' % (ZEMBEREK_PATH))
    
TurkishMorphology = JClass('zemberek.morphology.TurkishMorphology')
morphology = TurkishMorphology.createWithDefaults()
words_base = sql.takeSentence1("kelimeler.db", "roots_pos_flag")
def find_word(word):
    
    suggestion_word = "None"
    for i in range(0,len(words_base)):
        if word == words_base[i][0]:
            suggestion_word = words_base[i][2]
            break
        
    return suggestion_word

def find_root(word):               
    root = list()  
    analysis: java.util.ArrayList = (
        morphology.analyzeAndDisambiguate(word).bestAnalysis())
    
    for i, analysis in enumerate(analysis, start=0):
     
        root.append( f'{str(analysis.getLemmas()[0])}')
        
        
    return root[0]


def suggestion(sentence):
    words = sentence.split()
    
    for word in words:
        root = find_root(word)
        if root!= "UNK":
            suggestion_word = find_word(root)
            if (suggestion_word == "X") or suggestion_word == "Turkish":
                continue
            elif suggestion_word == "None":
                 possible_word = dist.correction(word)
                 print("\""+word+"\""+" kelimesi yanlış yazılmıştır.Bunu mu demek istediniz? " + "\"" + possible_word[1] + "\"")
                 print("\n")
            else:
               print("\""+ word + "\""+ " kelimesi yabancı kökenlidir.")
               print("Bu kelime yerine " + "\""+ suggestion_word +"\"" + " kelimesi/kelimeleri kullanabilirsiniz.")
               print("\n")
            
        else:
            possible_word = dist.correction(word)
            print("\""+word+"\""+" kelimesi yanlış yazılmıştır.Bunu mu demek istediniz? " + "\"" + possible_word[1] + "\"")
            print("\n")
            
            
            
            
def suggestion_e(sentence,correction):
    words = sentence.split()
    new_sentence = ""
    if correction:
        for word in words:
            root = find_root(word)
            if root != "UNK":
                suggestion_word = find_word(root)
                if (suggestion_word  == "X") or (suggestion_word == "Turkish"):
                    new_sentence = new_sentence + word + " "
                elif suggestion_word == "None":
                    possible_word = dist.correction(word)
                    print("\""+word+"\""+" kelimesi yanlış yazılmıştır.Bunu mu demek istediniz? " + "\"" + possible_word[1][0] + "\"")
                    print("\n")
                    new_sentence = new_sentence + word  + " "
                else:
                   print("\""+ word + "\""+ " kelimesi yabancı kökenlidir.")
                   print("Bu kelime yerine " + "\""+ suggestion_word +"\"" + " kelimesi/kelimeleri kullanabilirsiniz.")
                   print("\n")
                   new_sentence = new_sentence + word + " "
            else:
                possible_word = dist.correction(word)
                new_sentence = new_sentence + possible_word[1][0] + " "
                    
        
        
    else:
        for word in words:
            root = find_root(word)
            if root!= "UNK":
                suggestion_word = find_word(root)
                if (suggestion_word == "X") or suggestion_word == "Turkish":
                    continue
                elif suggestion_word == "None":
                    possible_word = dist.correction(word)
                    print("\""+word+"\""+" kelimesi yanlış yazılmıştır.Bunu mu demek istediniz? " )
                    for i in possible_word[1]:
                        print(i)
                    print("\n")
                else:
                   print("\""+ word + "\""+ " kelimesi yabancı kökenlidir.")
                   print("Bu kelime yerine " + "\""+ suggestion_word +"\"" + " kelimesi/kelimeleri kullanabilirsiniz.")
                   print("\n")
                
            else:
                possible_word = dist.correction(word)
                print("\""+word+"\""+" kelimesi yanlış yazılmıştır.Bunu mu demek istediniz? " )
                for i in possible_word[1]:
                    print(i)
                print("\n")
        
        
    return new_sentence        

    
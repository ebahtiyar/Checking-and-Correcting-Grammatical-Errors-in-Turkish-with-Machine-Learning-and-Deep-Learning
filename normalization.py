  # -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 15:53:28 2022

@author: emreb
"""
import time
import suggestion_word as sugg
print("Active suggestion_word")
time.sleep(0.5)
import model_de_da as de_da
print("Active model_de_da")
time.sleep(0.5)
import model_ki as ki
print("Active model_ki")
time.sleep(0.5)
import model_punc as punc
print("Active model_punc")
time.sleep(0.5)

    

def normalization(sentence,correction):

    de_da_sentence = de_da.model_de_da_prediction(sentence)
    ki_sentence = ki.model_ki_prediction(de_da_sentence)
    correction_sentence = sugg.suggestion_e(ki_sentence,correction).strip()
    if len(correction_sentence) > 1:
        punc_sentence = punc.prediction(correction_sentence)
    else:
        punc_sentence = punc.prediction(ki_sentence)

    punc_sentence = punc_sentence.capitalize()
    return punc_sentence

#yanlız hatalı manuel ekle
#Orginal Bu agresif tavırların onların da canını sıkmaya başladı. 
sentence = "bu agresif tavırların onlarında canını sıkmaya başladı"

#Orginal Asistana verilen doküman benimki ile aynı mıydı?
sentence1 = "asistanada verilen doküman benim ki ilee aynı mıydı"

#Orginal çarşamba ve perşembe günlerinde ders yapılmayacak mıymış?.
sentence2 ="çarşamba ve perşembe günlerin de ders yapılmıyacak mıymış"

#Orginal Ben de yaptım  ama onunki daha güzel oldu yine de.
sentence3 = "bende yaptım ama onun ki daha güzeel oldu yinede"

#Orginal Evde de elma, portakal kalmamış.
sentence4 = "evdede elma portakal kalmamış"
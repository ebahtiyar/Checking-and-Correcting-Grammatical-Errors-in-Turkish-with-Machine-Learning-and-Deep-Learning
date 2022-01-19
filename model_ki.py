# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 15:19:23 2022

@author: emreb
"""

from keras.models import load_model
import re
import os
from gensim.models import Word2Vec
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences


model_main  = load_model(os.path.join("C:/Users/emreb/Desktop/main_proje/models/model_ki",'model_ki_w2v_1.h5'))
idx2Label = {0 :'PAD', 1:'UNK' , 2: 'o' , 3: 'e'}
Word2Vec_model=Word2Vec.load("C:/Users/emreb/Desktop/main_proje/models/model_ki/Word2Vec_model_ki")


def replace_str_index(text,index=0,replacement=''):
    return '%s%s%s'%(text[:index],replacement,text[index+1:])



def word_tokenizer_ki(line):
        line = re.sub(r'[^\w\s]', '', line)
        words = line.split()
        r_words = []
        try:
            for pos,word in enumerate(words):
                n = ""
                if pos > 0:
                   if word == "ki":
                      before_word = words[pos-1]
                      n = before_word + " ki"
                      r_words.remove(before_word)
                      r_words.append(n)
                   else:
                       r_words.append(word)
                else:
                    r_words.append(word)
        except:
            pass
                
        return r_words
    
    
    
    
def model_ki_prediction(sample):
  sample_pad = []
  words = word_tokenizer_ki(sample.lower())
  for word in words:
      if word in Word2Vec_model.wv.index_to_key:
          
         sample_pad.append(Word2Vec_model.wv.key_to_index[word])
      else:
         sample_pad.append(Word2Vec_model.wv.key_to_index["UNK"])

  sample_pad = pad_sequences([sample_pad], maxlen=34, padding='post')

  pred = model_main.predict(sample_pad)
  label = [idx2Label[np.argmax(x)] for x in pred[0]]
  output_label = ""
  for i in label:
      output_label = output_label + i + " "

  pred_sent = ""
  for i in zip(words,label):
    if i[1] == "o":
      pred_sent = pred_sent +  i[0] + " "
    elif i[1] == "e":
        if i[0].find(" ki") > 0:
            new_word = replace_str_index(i[0],index=i[0].find(" ki"),replacement='')
            pred_sent = pred_sent + new_word + " "
        elif i[0].find(" ") == -1 and i[0].find("ki") == len(i[0]) - 2:
            new_word = replace_str_index(i[0],i[0].find("ki"),replacement=' k')
            pred_sent = pred_sent + new_word + " "
        else:
            pred_sent = pred_sent + i[0] + " "
            
    elif i[0][1] == "PAD":
        continue
  pred_sent = pred_sent.strip()

  return pred_sent    
    
    

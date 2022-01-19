# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 15:43:06 2022

@author: emreb
"""

import pickle
from keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import os 
import numpy as np

model_main  = load_model(os.path.join("C:/Users/emreb/Desktop/main_proje/models/model_punc",'model_punc_1.h5'))
with open('C:/Users/emreb/Desktop/main_proje/models/model_punc/in_train_tokenizer_punc', 'rb') as handle:
    in_train_tokenizer = pickle.load(handle)


with open('C:/Users/emreb/Desktop/main_proje/models/model_punc/out_train_tokenizer_punc', 'rb') as handle:
    out_train_tokenizer = pickle.load(handle)
    
    
    
def prediction(sample):
  sample = sample.lower()
  sample_pad = []
  for word in sample.split():
      if word in in_train_tokenizer.word_index:
         sample_pad.append(in_train_tokenizer.word_index[word])
      else:
         sample_pad.append(1)

  sample_pad = pad_sequences([sample_pad], maxlen=34, padding='post')
  pred = model_main.predict(sample_pad)
  y_id_to_word = {value: key for key, value in out_train_tokenizer.word_index.items()}
  y_id_to_word[0] = '<PAD>'
  puncs = [y_id_to_word[np.argmax(x)] for x in pred[0]]
  new_sentence = ""
  words = sample.split()
  for n,word in enumerate(words):
     if puncs[n] == "emp":
        new_sentence = new_sentence + word + " "
     if puncs[n] == "com":
        new_sentence = new_sentence + word + ", "
     if puncs[n] == "per":
        new_sentence = new_sentence + word + ".  "    
     if puncs[n] == "que":
        new_sentence = new_sentence + word + "?  "
     if puncs[n] == "<PAD>":
        continue
  
  return new_sentence.strip()
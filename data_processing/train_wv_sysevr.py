#!/usr/bin/env python
# coding: utf-8

# In[4]:


import argparse
from gensim.models import Word2Vec
import json
import os


def train(data_paths, save_model_dir, model_name='li_et_al_wv', min_occ=1, embedding_size=64, epochs=5):
    files = data_paths
    sentences = []
    for f in files:
        data = json.load(open(f))
        for e in data:
            code = e['tokenized']
            sentences.append([token.strip() for token in code.split()])
    print(len(sentences))
    wvmodel = Word2Vec(sentences, min_count=min_occ, workers=8, size=embedding_size)
    print('Embedding Size : ', wvmodel.vector_size)
    for i in range(epochs):
        wvmodel.train(sentences, total_examples=len(sentences), epochs=1)
    if not os.path.exists(save_model_dir):
        os.mkdir(save_model_dir)
    save_file_path = os.path.join(save_model_dir, model_name)
    wvmodel.save(save_file_path)



# In[5]:


files = [
    '../data/SySeVR/Arithmetic_expression-processed.json', 
    '../data/SySeVR/API_function_call-processed.json',
    '../data/SySeVR/Array_usage-processed.json',
    '../data/SySeVR/Pointer_usage-processed.json'
]

train(files, '../data/Word2Vec')


# In[ ]:





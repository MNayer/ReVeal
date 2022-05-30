#!/usr/bin/env python
# coding: utf-8

# In[4]:


import os, sys

output_data = '../data/draper/juliet.json'

input_code = '../data/draper/juliet.data'
input_label = '../data/draper/juliet.label'


# In[7]:


full_data = []
all_tokenized = []

with open(input_code) as code_file:
    with open(input_label) as label_file:
        for idx, (code, label) in enumerate(zip(code_file, label_file)):
            if idx % 1000 == 0:
                print(idx)
            code_tokens  = [t.strip() for t in code.strip().split()]
            label = int(label.strip())
            for i in range(len(code_tokens)):
                if code_tokens[i] == 'IDENT':
                    code_tokens[i] = "ID"
                elif code_tokens[i] == 'VARIABLE_NAME':
                    code_tokens[i] = "ID"
                    pass
                elif code_tokens[i] == 'FUNCTION_NAME':
                    code_tokens[i] = "ID"
                    pass
            data_point = {
                'code': code.strip(),
                'label': label,
                'tokenized': ' '.join(code_tokens)
            }
            all_tokenized.append(' '.join(code_tokens))
            full_data.append(data_point)
            

            


# In[8]:


len(all_tokenized)


# In[9]:


len(set(all_tokenized))


# In[10]:


63516/202462


# In[11]:


import json 
fp = open(output_data, 'w')
json.dump(full_data, fp)
fp.close()


# In[12]:


100-31.37


# In[ ]:





#!/usr/bin/env python
# coding: utf-8

# In[1]:


import warnings
warnings.filterwarnings('ignore')

import h5py

train_file_name = '../data/draper/raw/VDISC_train.hdf5'
train_file = h5py.File(train_file_name)

import clang.cindex
import clang.enumerations
import csv
import numpy as np
import os
# set the config
clang.cindex.Config.set_library_path("/usr/lib/x86_64-linux-gnu")
clang.cindex.Config.set_library_file('/usr/lib/x86_64-linux-gnu/libclang-6.0.so.1')



# In[2]:


import re 

class Tokenizer:
    # creates the object, does the inital parse
    def __init__(self, path, tokenizer_type='original'):
        self.index = clang.cindex.Index.create()
        self.tu = self.index.parse(path)
        self.path = self.extract_path(path)
        self.symbol_table = {}
        self.symbol_count = 1
        self.tokenizer_type = tokenizer_type

    # To output for split_functions, must have same path up to last two folders
    def extract_path(self, path):
        return "".join(path.split("/")[:-2])

    
    def full_tokenize_cursor(self, cursor):
        tokens = cursor.get_tokens()
        result = []
        for token in tokens:
            if token.kind.name == "COMMENT":
                continue
            if token.kind.name == "LITERAL":
                result += self.process_literal(token)
                continue
            if token.kind.name == "IDENTIFIER":
                result += ["ID"]
                continue
            result += [token.spelling]
        return result

    def full_tokenize(self):
        cursor = self.tu.cursor
        return self.full_tokenize_cursor(cursor)

    def process_literal(self, literal):
        cursor_kind = clang.cindex.CursorKind
        kind = literal.cursor.kind
        if kind == cursor_kind.INTEGER_LITERAL:
            return literal.spelling
        if kind == cursor_kind.FLOATING_LITERAL:
            return literal.spelling
        if kind == cursor_kind.IMAGINARY_LITERAL:
            return ["NUM"]       
        if kind == cursor_kind.STRING_LITERAL:
            return ["STRING"]
        sp = literal.spelling
        if re.match('[0-9]+', sp) is not None:
            return sp
        return ["LITERAL"]

    def split_functions(self, method_only):
        results = []
        cursor_kind = clang.cindex.CursorKind
        cursor = self.tu.cursor
        for c in cursor.get_children():
            filename = c.location.file.name if c.location.file != None else "NONE"
            extracted_path = self.extract_path(filename)

            if (c.kind == cursor_kind.CXX_METHOD or (method_only == False and c.kind == cursor_kind.FUNCTION_DECL)) and extracted_path == self.path:
                name = c.spelling
                tokens = self.full_tokenize_cursor(c)
                filename = filename.split("/")[-1]
                results += [tokens]

        return results
    

def tokenize(file_text):
    try:
        c_file = open('/tmp/test1.c', 'w')
        c_file.write(file_text)
        c_file.close()
        tok = Tokenizer('/tmp/test1.c')
        results = tok.split_functions(False)
        return ' '.join(results[0])
    except:
        return None


# In[3]:


list(train_file)


# In[4]:


num_vul = 0
num_non_vul = 0
vul_indices = []

for idx, (a, b, c, d, e) in  enumerate(zip(
    train_file['CWE-119'], train_file['CWE-120'], train_file['CWE-469'], 
    train_file['CWE-476'], train_file['CWE-other']
)):
    if a or b or c or d or e:
        num_vul += 1
        vul_indices.append(idx)
    else:
        num_non_vul += 1

print(num_vul, num_non_vul, len(vul_indices))


# In[5]:


print(tokenize("int main(){\n\tint *a = new int[10];\n\treturn 50;\n}\n"))
ratio = 65907 / float(953567)
print(ratio)


# In[6]:


sources = []
v, nv = 0, 0
import numpy as np

for idx, func in enumerate(train_file['functionSource']):
    if idx % 10000 == 0:
        print(idx, v, nv)
    if idx in vul_indices:
        tokenized = tokenize(func.strip())
        if tokenize is None:
            continue
        sources.append({'code': func.strip(), 'label': 1, 'tokenized': tokenized})
        v += 1
    else:
        r = np.random.uniform()
        if r <= 1.00:
            tokenized = tokenize(func.strip())
            if tokenize is None:
                continue
            sources.append({'code': func.strip(), 'label': 0, 'tokenized': tokenized})
            nv += 1



# In[7]:


len(sources)
import json


# In[8]:


train_file_name = open('../data/draper/train_full.json', 'w')
json.dump(sources, train_file_name)
train_file_name.close()
print(sources[0])


# In[16]:


def get_all(file_path):
    _file = h5py.File(file_path)
    v = 0
    nv = 0
    sources = []
    for idx, (a, b, c, d, e, f) in  enumerate(zip(
        _file['CWE-119'], _file['CWE-120'], _file['CWE-469'], 
        _file['CWE-476'], _file['CWE-other'], _file['functionSource']
    )):
        if idx % 10000 == 0:
            print(idx)
        tokenized = tokenize(f)
        if tokenized == None:
            continue
        if a or b or c or d or e:
            sources.append({
                'code': f.strip(),
                'label': 1,
                'tokenized': tokenized
            })
            v += 1
        else:
            sources.append({
                'code': f.strip(),
                'label': 0,
                'tokenized': tokenized
            })
            nv += 1
    return sources, v, nv


# In[20]:


valid_file_name = '../data/draper/VDISC_validate.hdf5'
valid_data, v, nv = get_all(valid_file_name)
print(v, nv, len(valid_data), valid_data[0])


# In[21]:


json_file_name = open('../data/draper/valid.json', 'w')

json.dump(valid_data, json_file_name)
json_file_name.close()


# In[22]:


test_file_name = '../data/draper/VDISC_test.hdf5'
test_data, v, nv = get_all(test_file_name)
print(v, nv, len(test_data))
json_file_name = open('../data/draper/test.json', 'w')

json.dump(test_data, json_file_name)
json_file_name.close()


# In[ ]:





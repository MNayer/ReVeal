#!/usr/bin/env python
# coding: utf-8

# In[28]:


edgeType_full = {
    'IS_AST_PARENT': 1,
    'IS_CLASS_OF': 2,
    'FLOWS_TO': 3,
    'DEF': 4,
    'USE': 5,
    'REACHES': 6,
    'CONTROLS': 7,
    'DECLARES': 8,
    'DOM': 9,
    'POST_DOM': 10,
    'IS_FUNCTION_OF_AST': 11,
    'IS_FUNCTION_OF_CFG': 12
}

import csv

def inputGeneration(nodeCSV, edgeCSV, edge_type_map=edgeType_full, cfg_only=False):
    gInput = dict()
    gInput["targets"] = list()
    gInput["graph"] = list()
    gInput["node_features"] = list()
    gInput["targets"].append([1])
    with open(nodeCSV, 'r') as nc:
        nodes = csv.DictReader(nc, delimiter='\t')
        nodeMap = dict()
        allNodes = {}
        node_idx = 0
        for idx, node in enumerate(nodes):
            print(node.keys())
            cfgNode = node['isCFGNode'].strip()
            if not cfg_only and (cfgNode == '' or cfgNode == 'False'):
                continue
            nodeKey = node['key']
            node_type = node['type']
            if node_type == 'File':
                continue
            node_content = node['code'].strip()
#             node_split = nltk.word_tokenize(node_content)
#             nrp = np.zeros(100)
#             for token in node_split:
#                 try:
#                     embedding = wv.wv[token]
#                 except:
#                     embedding = np.zeros(100)
#                 nrp = np.add(nrp, embedding)
#             if len(node_split) > 0:
#                 fNrp = np.divide(nrp, len(node_split))
#             else:
#                 fNrp = nrp
#             node_feature = type_one_hot[type_map[node_type] - 1].tolist()
            node_feature = [node_content, node['location']]
            allNodes[nodeKey] = node_feature
            nodeMap[nodeKey] = node_idx
            node_idx += 1
        if node_idx == 0 or node_idx >= 500:
            return None
        all_nodes_with_edges = set()
        trueNodeMap = {}
        all_edges = []
        with open(edgeCSV, 'r') as ec:
            reader = csv.DictReader(ec, delimiter='\t')
            for e in reader:
                start, end, eType = e["start"], e["end"], e["type"]
                if eType != "IS_FILE_OF":
                    if not start in nodeMap or not end in nodeMap or not eType in edge_type_map:
                        continue
                    all_nodes_with_edges.add(start)
                    all_nodes_with_edges.add(end)
                    edge = [start, edge_type_map[eType], end]
                    all_edges.append(edge)
        if len(all_edges) == 0:
            return None
        for i, node in enumerate(all_nodes_with_edges):
            trueNodeMap[node] = i
            gInput["node_features"].append(allNodes[node])
        for edge in all_edges:
            start, t, end = edge
            start = trueNodeMap[start]
            end = trueNodeMap[end]
            e = [start, t, end]
            gInput["graph"].append(e)
    return gInput


# In[29]:


base = '/home/saikatc/DATA/CCS-Vul_Det/data/neurips_parsed/parsed_results/1667_FFmpeg_5c720657c23afd798ae0db7c7362eb859a89ab3d_1.c/'
nodes = base + 'nodes.csv'
edges = base + 'edges.csv'
graph = inputGeneration(nodes, edges)


# In[30]:


print(len(graph["node_features"]))


# In[31]:


activation = [
    [0.04348256066441536, 0.003500928869470954], [0.00987162534147501, 0.04583273082971573], 
    [-0.24319593608379364, 0.0013916491298004985], [0.3781493306159973, 0.7286356687545776], 
    [0.755454957485199, 0.7855706214904785], [-0.025368133559823036, 0.006620634812861681], 
    [-0.09509257227182388, -0.24337084591388702], [-0.0036633836571127176, 0.07984677702188492], 
    [-0.09028370678424835, 0.5313823819160461], [0.03486397862434387, 0.08663380146026611], 
    [-0.0497242733836174, -0.0850924476981163], [0.023616140708327293, -0.1634553223848343], 
    [-0.008202042430639267, 0.002261550398543477], [0.03686459735035896, -0.0407043881714344], 
    [0.5247610807418823, -0.029690468683838844], [0.27675679326057434, 0.01650792360305786], 
    [-0.0209635142236948, 0.0011175392428413033], [-0.012501797638833523, -0.0035343982744961977], 
    [0.00333977397531271, -0.00986259151250124], [0.21612189710140228, 1.1710708141326904], 
    [0.0013831312535330653, 0.016146864742040634], [0.09524355083703995, 0.04426507651805878], 
    [0.023414066061377525, 0.027849748730659485]
]


# In[32]:


nodes = graph["node_features"]
print(activation)


# In[33]:


diff_act = [a[1]-a[0] for a in activation]


# In[48]:


min_a = min(diff_act)
max_a = max(diff_act)
d = max_a-min_a
norm_a = [ round((a-min_a)/d, 3) for a in diff_act]
print(norm_a)
bins = []
for a in norm_a:
    if a < 0.2:
        bins.append('\lfive')
    elif a < 0.4:
        bins.append('\lfour')
    elif a < 0.6:
        bins.append('\lthree')
    elif a < 0.8:
        bins.append('\ltwo')
    else:
        bins.append('\lone')


# In[49]:


tuples = []
for nidx, (n, a, b) in enumerate(zip(nodes, norm_a, bins)):
    if ':' in n[1]:
        ln = int(n[1].strip().split(':')[0])
    else:
        ln = 0
    tuples.append((nidx, n[0], ln, a, b))
sorted_tuples = sorted(tuples, key=lambda x:x[2])
for t in sorted_tuples:
    print(*t, sep='\t')


# In[46]:


edges = graph['graph']
print(edges)


# In[47]:


types = set([t[0] for t in edges])
print(types)


# In[ ]:





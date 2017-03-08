import numpy as np
from os import listdir
from os.path import isfile, join
import networkx as nx
from tqdm import tqdm
# import sys

# First get a list of valid ego users
GPLUS_DIR = "dataset/gplus/"
ego_users = np.unique(
    map(
        lambda f : f.split('.')[0],
        [f for f in listdir(GPLUS_DIR) if isfile(join(GPLUS_DIR, f))]
    )
)

G = nx.DiGraph()


encode_kv_count = 0
def encode_kv(d, t):
    global encode_kv_count
    if t in d:
        return d[t]
    else:
        d[t] = encode_kv_count
        encode_kv_count += 1
        return encode_kv_count - 1


encode_k_count = 0
def encode_k(d, k):
    global encode_k_count
    if k in d:
        return d[k]
    else:
        d[k] = encode_k_count
        encode_k_count += 1
        return encode_k_count - 1

vertex_count = 0
def encode_vertex(d, v):
    global vertex_count
    if v in d:
        return d[v]
    else:
        d[v] = vertex_count
        vertex_count += 1
        return vertex_count - 1

# Encodings
k_dict = {}
kv_dict = {}
v_dict = {}

# Parse the featnames
propnames = []
propvalues = []

print "Extracting vertex data"
for ego_user in tqdm(ego_users):

    with open(join(GPLUS_DIR, ego_user + '.featnames'), 'r') as fnf:
        for line in fnf:
            vid, prop = line.rstrip().split(' ', 1)
            propname, value = prop.split(':', 1)

            propnames.append(propname)
            propvalues.append(value)

    # Insert the ego node itself
    G.add_node(encode_vertex(v_dict, int(ego_user)))

    # Fetch the ego nodes properties
    with open(join(GPLUS_DIR, ego_user + '.egofeat'), 'r') as efeat:
        arr = np.fromfile(efeat, sep=' ', dtype=int)
        indexes, = np.nonzero(arr)
        for i in indexes:
            v = encode_vertex(v_dict, int(ego_user))
            prop = encode_k(k_dict, propnames[i])
            val = encode_kv(kv_dict, (propnames[i], propvalues[i]))
            G.node[v][prop] = val

    # Fetch properties for all other nodes
    with open(join(GPLUS_DIR, ego_user + '.feat'), 'r') as feat:
        for line in feat:
            try:
                vertex, arr = line.rstrip().split(' ', 1)
                arr = np.fromstring(arr, sep=' ', dtype=int)
            except ValueError:
                # This node has no attributes probably!
                pass
            indexes, = np.nonzero(arr)

            # Add vertex to graph
            v = encode_vertex(v_dict, int(vertex))
            G.add_node(v)

            # Add properties to graph
            for i in indexes:
                prop = encode_k(k_dict, propnames[i])
                val = encode_kv(kv_dict, (propnames[i], propvalues[i]))
                G.node[v][prop] = val

print "Extracting edge data"
with open(join('dataset', 'gplus_combined.txt')) as edata:
    for line in tqdm(edata):
        u, v = line.rstrip().split(' ')
        u = encode_vertex(v_dict, int(u))
        v = encode_vertex(v_dict, int(v))
        G.add_edge(u, v)


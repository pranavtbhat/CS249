import numpy as np
from os import listdir
from os.path import isfile, join
import networkx as nx
from tqdm import tqdm

# First get a list of valid ego users
GPLUS_DIR = "dataset/gplus/"
ego_users = np.unique(
    map(
        lambda f : f.split('.')[0],
        [f for f in listdir(GPLUS_DIR) if isfile(join(GPLUS_DIR, f))]
    )
)

G = nx.DiGraph()

print "Extracting vertex data"
for ego_user in tqdm(ego_users):

    # Parse the featnames
    propnames = []
    propvalues = []

    with open(join(GPLUS_DIR, ego_user + '.featnames'), 'r') as fnf:
        for line in fnf:
            vid, prop = line.rstrip().split(' ', 1)
            propname, value = prop.split(':', 1)
            propnames.append(propname)
            propvalues.append(value)

    # Insert the ego node itself
    G.add_node(int(ego_user))

    # Fetch the ego nodes properties
    with open(join(GPLUS_DIR, ego_user + '.egofeat'), 'r') as efeat:
        arr = np.fromfile(efeat, sep=' ', dtype=int)
        indexes, = np.nonzero(arr)
        for i in indexes:
            G[int(ego_user)][propnames[i]] = propvalues[i]

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
            G.add_node(int(vertex))

            # Add properties to graph
            for i in indexes:
                G[int(vertex)][propnames[i]] = propvalues[i]

print "Extracting edge data"
with open(join('dataset', 'gplus_combined.txt')) as edata:
    for line in tqdm(edata):
        u, v = line.rstrip().split(' ')
        G.add_edge(int(u), int(v))

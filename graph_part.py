import networkx as nx
import pandas as pd
from os.path import join
import metis
from tqdm import tqdm

G = nx.Graph()
vertex_dict = {}

vertex_count = 0
def encode_vertex(d, v):
    global vertex_count
    if v in d:
        return d[v]
    else:
        d[v] = vertex_count
        vertex_count += 1
        return vertex_count - 1


print "Adding vertices and vertex data"
data = pd.read_csv(
    'processed_vertex_data.tsv',
    dtype= {'vertex_id' : str, 'gender' : str, 'university' : str, 'place' : str, 'institution' : str, 'job_title' : str},
    delimiter = "\t"
)
data = data.where((pd.notnull(data)), None)
print data.shape

for i,vertex in tqdm(enumerate(data.vertex_id.values)):
    v = encode_vertex(vertex_dict, vertex)
    data.set_value(i, 'vertex_id', v)

    G.add_node(v)
    row = data.iloc[i][1:]
    for key, value in enumerate(row):
        G.node[v][key] = value

data.to_csv('vertex_data_encoded.tsv', sep='\t')

print "Extracting edge data"
with open(join('dataset', 'gplus_combined.txt')) as edata:
    for line in edata:
        u, v = line.rstrip().split(' ')
        u = encode_vertex(vertex_dict, u)
        v = encode_vertex(vertex_dict, v)
        G.add_edge(u, v)

print "Partitioning Graph"
edge_cuts, parts = metis.part_graph(G, 10)
indices = pd.DataFrame({'indices' : parts}).groupby(by='indices').groups

for i, part in indices.iteritems():
    print "Subgraphing in ", i
    graph = nx.Graph(G.subgraph(list(part)))
    print "Writing in ", i
    nx.write_gexf(graph, "Graph{}.gexf".format(i))


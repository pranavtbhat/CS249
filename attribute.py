from sklearn.feature_extraction.text import TfidfVectorizer
import networkx as nx
import numpy as np
import random
import itertools
from tqdm import tqdm

def mine_text_fields(g):
    # Extract text_fields from vertices
    text_job_title = [g.node[u]['6'] for u in g.nodes()]
    text_last_name = [g.node[u]['1'] for u in g.nodes()]

    # Generate TF-IDF matrices for text fields
    vect_job_title = TfidfVectorizer(min_df=1)
    vect_last_name = TfidfVectorizer(min_df=1)

    tfidf_job_title = vect_job_title.fit_transform(text_job_title)
    tfidf_last_name = vect_last_name.fit_transform(text_last_name)

    # Compute Pairwise similarities for text fields
    print "Computing similarity scores for Job-Titles"
    similarity_job_title = (tfidf_job_title * tfidf_job_title.T).A

    print "Computing similarity scores for Last-Names"
    similarity_last_name = (tfidf_last_name * tfidf_last_name.T).A

    return similarity_job_title, similarity_last_name

def attribute_similarity(
        g, # Graph
        u, # From vertex
        v, # To vertex
        similarity_job_title, # VxV similarities for job-titles
        similarity_last_name, # VxV similarities for last-names
        weights = [0, 0, 1, 1, 1, 1, 0] # Weights for features
    ):
    score = 0
    u_att = g.node[u]
    v_att = g.node[v]

    ###
    # Attribute MAP
    # 0 - vertex_id
    # 1 - last_name
    # 2 - gender
    # 3 - university
    # 4 - place,
    # 5 - institution
    # 6 - job_title
    ###

    # Attribute 0 - Vertex_id
    # SKIP!!

    # Attribute 1 - last_name
    score += weights[0] * similarity_last_name[u,v]

    # Attribute 2 - gender
    score += weights[1] * (u_att['2'] == v_att['2'])

    # Attribute 3 - university
    intersect = len(set(u_att['3']) & set(v_att['3']))
    score += weights[2] * intersect

    # Attribute 4 - place
    intersect = len(set(u_att['4']) & set(v_att['4']))
    score += weights[3] * intersect

    # Atribute 5 - institution
    intersect = len(set(u_att['5']) & set(v_att['5']))
    score += weights[4] * intersect

    # Attribute 6 - job_title
    score += weights[5] * similarity_job_title[u,v]

    return score

def make_sim_matrix(g, weights=[0, 0, 1, 1, 1, 1, 0]):
    # Make a matrix with our similarities
    V = g.number_of_nodes()
    M = np.zeros((V, V))

    similarity_job_title, similarity_last_name = mine_text_fields(g)

    for (u,v) in tqdm(itertools.combindations(g.nodes(), 2), total=(V * (V-1))/2):
        sim = attribute_similarity(g, u, v, similarity_job_title, similarity_last_name, weights)
        M[u,v] = sim
        M[v,u] = sim

    return M


def make_nx_matrix(g, alg = nx.resource_allocation_index):
    V = g.number_of_nodes()
    M = np.zeros((V, V))

    for e in tqdm(itertools.combindations(g.nodes(), 2), total=(V * (V-1))/2):
        sim = alg(g, e)
        M[u,v] = sim
        M[v,u] = sim

    return M


if __name__ == "__main__":
    ###
    # Set weights here
    ###
    weights = [0, 0, 1, 1, 1, 1, 0]

    # Do some basic similarity checking for all graphs
    for graph_no in range(10):
        print "Loading Graph{}.gexf".format(graph_no)
        g = nx.convert_node_labels_to_integers(nx.read_gexf('dataset/processed/Graph{}.gexf'.format(graph_no)))
        sample_nodes = random.sample(g.nodes(), 1000)

        # Print some Graph stats
        print "Number of nodes:", g.number_of_nodes()
        print "Number of edges:", g.number_of_edges()

        similarity_job_title, similarity_last_name = mine_text_fields(g)

        print "Average similarity score for edges is:", np.mean(
            [attribute_similarity(g, u, v, similarity_job_title, similarity_last_name, weights) for (u,v) in g.edges()]
        )

        print "Average simialrity score for a large random sample is:", np.mean(
            [attribute_similarity(g, u, v, similarity_job_title, similarity_last_name, weights) for (u,v) in itertools.combinations(sample_nodes, 2)]
        )


        print "Average link pred score for edges is:", np.mean(
            [w for (u,v,w) in nx.resource_allocation_index(g, g.edges())]
        )

        print "Average link pred score for a large random sample is:", np.mean(
            [w for (u,v,w) in nx.resource_allocation_index(g, itertools.combinations(sample_nodes, 2))]
        )


        print "----------------"


from sklearn.feature_extraction.text import TfidfVectorizer
import networkx as nx
import numpy as np
import random
import itertools
from tqdm import tqdm
import scipy.optimize as scp
from bisect import bisect

nx_multiplier = 347.7343261

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
        weights = [0, 0, 0, 2, 2, 2, 1] # Weights for features
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
    score += weights[1] * similarity_last_name[u,v]

    # Attribute 2 - gender
    score += weights[2] * (u_att['2'] == v_att['2'])

    # Attribute 3 - university
    intersect = len(set(u_att['3']) & set(v_att['3']))
    score += weights[3] * intersect

    # Attribute 4 - place
    intersect = len(set(u_att['4']) & set(v_att['4']))
    score += weights[4] * intersect

    # Atribute 5 - institution
    intersect = len(set(u_att['5']) & set(v_att['5']))
    score += weights[5] * intersect

    # Attribute 6 - job_title
    score += weights[6] * similarity_job_title[u,v]

    return score

def make_sim_matrix(g, weights, alg=nx.adamic_adar_index):
    # Make a matrix with our similarities
    V = g.number_of_nodes()
    M = np.zeros((V, V))
    similarity_job_title, similarity_last_name = mine_text_fields(g)

    for (u,v,w) in tqdm(alg(g, itertools.combinations(g.nodes(), 2), total=(V * (V-1))/2)):
        sim = attribute_similarity(g, u, v, similarity_job_title, similarity_last_name, weights)
        M[u,v] = sim + nx_multiplier * w
        M[v,u] = sim + nx_multiplier * w

    return M


def make_nx_matrix(g, alg = nx.adamic_adar_index):
    # Fill a matrix with topology based similarities
    V = g.number_of_nodes()
    M = np.zeros((V, V))

    for (u,v,w) in tqdm(alg(g, itertools.combinations(g.nodes(), 2)), total=(V * (V-1))/2):
        M[u,v] = w
        M[v,u] = w

    return M

def compute_ranks(M, edges):
    # Given a matrix with similarity values, compute ranks
    V,_ = M.shape
    non_zeros_vals = sorted(M[M.nonzero()])
    return [bisect(non_zeros_vals, M[u,v]) if M[u,v] > 0 else 0 for (u,v) in tqdm(edges)]


def optimize_this(weights):
    # Loss function to optimize
    difference = calc_similarity_true(weights) - calc_similarity_false(weights)
    difference = difference*(-1)
    return difference

def calc_similarity_true(g, similarity_job_title, similarity_last_name, weights):
    # Similarity for edges that exist
    attribute_similarity_true = [attribute_similarity(g, u, v, similarity_job_title, similarity_last_name, weights) for (u,v) in g.edges()]
    attribute_similarity_true_mean = np.mean(attribute_similarity_true)
    return attribute_similarity_true_mean

def calc_similarity_false(g, similarity_job_title, similarity_last_name, weights):
    attribute_similarity_false = [attribute_similarity(g, u, v, similarity_job_title, similarity_last_name, weights) for (u,v) in itertools.combinations(sample_nodes, 2)]
    attribute_similarity_false_mean = np.mean(attribute_similarity_false)
    return attribute_similarity_false_mean


if __name__ == "__main__":
    ###
    # Set weights here
    ###
    weights = [0.0, 1.79353282, 282.74981033, 4.48265987, 15.78264496, 9.85613404, 3.56814422]
    for item in weights:
        item = item/4

    # Do some basic similarity checking for all graphs
    for graph_no in range(1):
        graph_no = 1
        print "Loading Graph{}.gexf".format(graph_no)
        g = nx.convert_node_labels_to_integers(nx.read_gexf('dataset/processed/Graph{}.gexf'.format(graph_no)))
        sample_nodes = random.sample(g.nodes(), 1000)

        # Print some Graph stats
        print "Number of nodes:", g.number_of_nodes()
        print "Number of edges:", g.number_of_edges()

        similarity_job_title, similarity_last_name = mine_text_fields(g)

        print "Average similarity score for edges is:", calc_similarity_true(g, similarity_job_title, similarity_last_name, weights)
        print "Average simialrity score for a large random sample is:", calc_similarity_false(g, similarity_job_title, similarity_last_name, weights)
        result = scp.minimize(optimize_this, weights)

        link_prediction_true = [w for (u,v,w) in nx.resource_allocation_index(g, g.edges())]
        link_prediction_true_mean = np.mean(link_prediction_true)
        print "Average link pred score for edges resource_allocation_index is:", link_prediction_true_mean


        link_prediction_false = [w for (u,v,w) in nx.resource_allocation_index(g, itertools.combinations(sample_nodes, 2))]
        link_prediction_false_mean = np.mean(link_prediction_false)
        print "Average link pred score for a large random sample resource_allocation_index is:", link_prediction_false_mean

        M = make_sim_matrix(g, weights)
        N = make_nx_matrix(g, weights)

        ranks_sim = compute_ranks(M, g.edges())
        ranks_nx = compute_ranks(N, g.edges())

        print "----------------"

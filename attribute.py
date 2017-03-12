import numpy as np


def attribute_similarity(G, u, v):
    score = 0
    for i in range(1, 7):
        u_att = G.node[u].get(i)
        v_att = G.node[v].get(i)

        score += len(np.intersect(u_att, v_att))

    return score

def attribute_similarity(G, u, v):
    score = 0
    for i in range(1, 7):
        u_att = G.node[u].get(i)
        v_att = G.node[v].get(i)

        score += len(set(u_att) & set(v_att))

    return score

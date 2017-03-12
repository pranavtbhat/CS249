def attribute_similarity(G, u, v):
    score = 0
    for i in range(6):
        u_att = G.node[u].get(str(i), -1)
        v_att = G.node[v].get(str(i), -1)

        if u_att == -1 or v_att == -1:
            pass
        elif u_att != v_att:
            score -= 0.00
        else:
            score += 1

    return score > 1

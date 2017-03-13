def attribute_similarity(G, u, v, weights = [0.001, 0.001, 0.1, 0.1, 0.1, 0.1]):
    score = 0
    u_att = G.node[u]
    v_att = G.node[v]

    # vertex_id, last_name, gender, university, place, institution, job_title
    # Ignore

    # Attribute 2 - last_name
    if u_att[2] == v_att[2]:
        score += weights[2]
    else:
        score -= weights[2]

    # Attribute 3 - gender
    if u_att[3] == v_att[3]:
        score += weights[3]
    else:
        score -= weights[3]

    # Attribute 4 - university
    intersect = len(set(u_att[4]) & set(v_att[4]))
    score += weights[4] * (intersect if intersect > 0 else -1)

    # Attribute 5 - place
    intersect = len(set(u_att[5]) & set(v_att[5]))
    score += weights[5] * (intersect if intersect > 0 else -1)

    # Atribute 6 - institution
    intersect = len(set(u_att[6]) & set(v_att[6]))
    score += weights[6] * (intersect if intersect > 0 else -1)

    return score

import numpy as np
from os import listdir
from os.path import isfile, join
from tqdm import tqdm

###
# This file generates a DataFrame for user properties
# DataFrame heading:
# vertex_id, last_name, gender, university, place, institution, job_title
###

# First get a list of valid ego users
GPLUS_DIR = "dataset/gplus/"
ego_users = np.unique(
    map(
        lambda f : f.split('.')[0],
        [f for f in listdir(GPLUS_DIR) if isfile(join(GPLUS_DIR, f))]
    )
)

# Parse the featnames
propnames = []
propvalues = []

with open("vertex_data.tsv", "w") as out:

    out.write("\t".join(['vertex_id', 'last_name', 'gender', 'university', 'place', 'institution', 'job_title']) + "\n")

    for ego_user in tqdm(ego_users):
        with open(join(GPLUS_DIR, ego_user + '.featnames'), 'r') as fnf:
            for line in fnf:
                vid, prop = line.rstrip().split(' ', 1)
                propname, value = prop.split(':', 1)

                propnames.append(propname)
                propvalues.append(value)

        ego_props = {'gender':"", 'university':"", 'place':"", 'last_name':"", 'job_title':"", 'institution':""}

        # Fetch the ego nodes properties
        with open(join(GPLUS_DIR, ego_user + '.egofeat'), 'r') as efeat:
            arr = np.fromfile(efeat, sep=' ', dtype=int)
            indexes, = np.nonzero(arr)
            for i in indexes:
                if propnames[i] in ['gender', 'last_name', 'job_title']:
                    ego_props[propnames[i]] += " " + propvalues[i]
                else:
                    ego_props[propnames[i]] += "|" +  propvalues[i]

        out.write(str(ego_user) + "\t")
        out.write("\t".join([str(val) for val in ego_props.values()]))
        out.write("\n")

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

                v_props = {'gender':"", 'university':"", 'place':"", 'last_name':"", 'job_title':"", 'institution':""}

                for i in indexes:
                    if propnames[i] in ['gender', 'last_name', 'job_title']:
                        v_props[propnames[i]] += " " + propvalues[i]
                    else:
                        v_props[propnames[i]] += "|" + propvalues[i]

                out.write(str(vertex) + "\t")
                out.write("\t".join([str(val) for val in v_props.values()]))
                out.write("\n")

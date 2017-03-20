###
# CS249: Mining Information and Social Networks
# Research Project: Link Prediction using Vertex Attributes
###

# Dependencies
- Metis
    Available at : http://glaros.dtc.umn.edu/gkhome/fetch/sw/metis/metis-5.1.0.tar.gz
    run:
        make config shared=1
        make install

- Python 2.7.1
    - networkx
    - metis
    - numpy
    - matplotlib
    - nltk
    - tqdm
    - scipy
    - sklearn

# Instructions on how to run
./build.sh
    This downloads the datset from the Stanford Netowrk Analysis Platform, and extracts the files into the dataset/ directory

python generate_vertex_dataframe.py
    This file preprocesses the vertex data contained in the dataset. It first extracts raw features for ego-nodes and then for the neighbors
    of the ego node. Next it constructs a vertex dataframe, with text fields for each of the super categories, obtained by concatenting the
    individual raw features. The dataframe is written to vertex_data.tsv.

python process_vertex_data.py
    This file clusters the raw features using the heuristic labelling data present in labelling/. The file generates a more compact dataframe  at processed_vertex_data.tsv

python graph_part.py
    This file constructs the graph using the vertex dataframe produced earlier and the edge data provided in the dataset. It then relabels the vertexes using compact integer labels, and finally partitions the graph using Metis, and writes the final graphs to dataset/processed/.

python attribute.py
    This file contains methods that implement our actual algorithm, and evalute the results obtained.

from sklearn.feature_extraction.text import TfidfVectorizer
import networkx as nx

# Load pre-processed graph dataset
g = nx.convert_node_labels_to_integers(nx.read_gexf('dataset/processed/Graph5.gexf'))

# Extract text_fields from vertices
text_job_title = [g.node[u]['6'] for u in g.nodes()]
text_last_name = [g.node[u]['1'] for u in g.nodes()]

# Generate TF-IDF matrices for text fields
vect_job_title = TfidfVectorizer(min_df=1)
vect_last_name = TfidfVectorizer(min_df=1)

tfidf_job_title = vect_job_title.fit_transform(text_job_title)
tfidf_last_name = vect_last_name.fit_transform(text_last_name)

# Compute Pairwise similarities for text fields
similarity_job_title = (tfidf_job_title * tfidf_job_title.T).A
similarity_last_name = (tfidf_last_name * tfidf_last_name.T).A

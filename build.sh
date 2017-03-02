# Directory stuff
rm -rf dataset
mkdir dataset
cd dataset

# Download datasets
wget http://snap.stanford.edu/data/gplus.tar.gz
wget http://snap.stanford.edu/data/gplus_combined.txt.gz
wget http://snap.stanford.edu/data/readme-Ego.txt

# Uncompress directories
tar -xvzf gplus.tar.gz
gzip -d gplus_combined.txt.gz



# Install Metis
wget http://glaros.dtc.umn.edu/gkhome/fetch/sw/metis/metis-5.1.0.tar.gz
tar -xvzf metis-5.1.0.tar.gz
rm metis-5.1.0.tar.gz
cd metis-5.1.0
make
make install
make config shared=1

cd ..


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



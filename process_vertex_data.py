import pandas as pd
import numpy as np

data = pd.read_csv('vertex_data.tsv', delimiter="\t")

# Remove all duplicate rows
data = data.drop_duplicates(subset='vertex_id')
data = data.where((pd.notnull(data)), None)

###
# Substitutions
###

def replace(s, d):
    global invalid
    labels = []
    if s != None:
        for key, value in d.iteritems():
            s = s.replace(key, str(value))
        for word in s.split('|'):
            if not word.isdigit():
                invalid[word] = invalid.get(word, 0) + 1
            else:
                labels.append(int(word))

        return "".join([str(i) for i in np.sort(np.unique(labels)).tolist()])
    else:
        return ''
##
# Institution
# Mappings:
# 1. Entertainment - 1
# 2. Tech - 2
# 3. Business - 3
# 4. Finance - 4
# 5. Education - 5
# 6. Retail - 6
# 7. Government - 7
# 8. Invalid - 8
##
invalid = {}
institution_mappings = {"Entertainment" : 1, "Tech" : 2, "Business" : 3, "Finance" : 4, "Education" : 5, "Retail" : 6, "Government" : 7, "Invalid" : ''}
institution_value_mappings = {}

with open('labelling/institiution', "r") as f:
    for line in f:
        key, value = line.rstrip().split('<>')
        key = key.lstrip().rstrip()
        value = value.lstrip().rstrip()
        institution_value_mappings[key] = institution_mappings[value]

data['institution'] = map(lambda x : replace(x, institution_value_mappings), data['institution'])
invalid_institutions = map(lambda x : x[0], sorted(invalid.items(), key = lambda x : x[1], reverse=True))

##
# University
# Mappings:
# 1. MidWest - 1
# 2. East - 2
# 3. West - 3
# 4. Australia - 50
# 5. Canada - 100
# 6. MiddleEast - 150
# 7. Europe - 200
# 8. Asia - 250
# 9. SouthAmerica - 300
# 10. Invalid - 350
##
invalid = {}
university_mappings = {"MidWest" : 1, "East" : 2, "West" : 3, "Australia" : 4, "Canada" : 5, "MiddleEast" : 6, "Europe" : 7, "Asia" : 8, "SouthAmerica" : 9, "Invalid" : ''}
university_value_mappings = {}

with open('labelling/university', "r") as f:
    for line in f:
        try:
            key, value = line.rstrip().split('<>')
        except:
            print line
            break
        key = key.lstrip().rstrip()
        value = value.lstrip().rstrip()
        university_value_mappings[key] = university_mappings[value]

data['university'] = map(lambda x: replace(x, university_value_mappings), data['university'])
invalid_universities = map(lambda x : x[0], sorted(invalid.items(), key = lambda x : x[1], reverse=True))

##
# Place
##
invalid = {}
place_mappings = {"us_east" : 0, "us_mid" : 1, "us_west" : 2, "canada" : 3, "australia" : 4, "middle_east" : 5, "south_america" : 6, "africa" : 7, "asia" : 8, "europe" : 9}
place_value_mappings = {}

for key, value in place_mappings.iteritems():
    with open('labelling/places/' + key + '.txt', 'r') as f:
        for line in f:
            line = line.lstrip().rstrip()
            place_value_mappings[line] = value

data['place'] = map(lambda x: replace(x, place_value_mappings), data['place'])
invalid_places = map(lambda x : x[0], sorted(invalid.items(), key = lambda x : x[1], reverse=True))

# Write to file
data.to_csv('processed_vertex_data.tsv', sep = '\t')

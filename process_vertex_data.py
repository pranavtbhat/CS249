import pandas as pd
import numpy as np

data = pd.read_csv('vertex_data.tsv', delimiter="\t")

# Remove all duplicate rows
data = data.drop_duplicates(subset='vertex_id')
data = data.where((pd.notnull(data)), None)

###
# Substitutions
###

invalid = {}

def replace(s, d):
    global invalid
    labels = []
    if s != None:
        for key, value in institution_value_mappings.iteritems():
            s = s.replace(key, str(value))
        for word in s.split('|'):
            if not word.isdigit():
                invalid[word] = invalid.get(word, 0) + 1
            else:
                labels.append(int(word))

        return np.sort(np.unique(labels)).tolist()
    else:
        return None
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
institution_mappings = {"Entertainment" : 1, "Tech" : 2, "Business" : 3, "Finance" : 4, "Education" : 5, "Retail" : 6, "Government" : 7, "Invalid" : ''}
institution_value_mappings = {}

with open('labelling/institiution', "r") as f:
    for line in f:
        key, value = line.rstrip().split('<>')
        key = key.lstrip().rstrip()
        value = value.lstrip().rstrip()
        institution_value_mappings[key] = institution_mappings[value]

data['institution'] = map(lambda x : replace(x, institution_value_mappings), data['institution'])


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
university_mappings = {"MidWest" : 1, "East" : 2, "West" : 3, "Australia" : 50, "Canada" : 100, "MiddleEast" : 150, "Europe" : 200, "Asia" : 250, "SouthAmerica" : 300, "Invalid" : 350}
university_value_mappings = {}

with open('labelling/university', "r") as f:
    for line in f:
        key, value = line.rstrip().split('<>')
        key = key.lstrip().rstrip()
        value = value.lstrip().rstrip()
        university_value_mappings[key] = university_mappings[value]

data['university'] = map(lambda x: replace(x, university_value_mappings), data['university'])


##
# Place
##
place_mappings = {"us_east" : 1, "us_mid" : 2, "us_west" : 3, "canada" : 50, "australia" : 100, "middle_east" : 150, "south_america" : 200, "africa" : 250, "asia" : 300}
place_value_mappings = {}

for key, value in place_mappings.iteritems():
    with open('labelling/places/' + key + '.txt', 'r') as f:
        for line in f:
            line = line.lstrip().rstrip()
            place_value_mappings[line] = value

data['place'] = map(lambda x: replace(x, place_value_mappings), data['place'])

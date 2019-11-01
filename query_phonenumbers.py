import requests
import json

osm_id_blacklist = [4348240589]

overpass_url = "http://overpass-api.de/api/interpreter"
overpass_query = """
[out:json];

area
  [wikidata=Q39]->.searchArea;

( //get all phones in the area
node
  ["amenity"="telephone"]
  ["phone"]
  (area.searchArea);

node
  ["amenity"="telephone"]
  ["contact:phone"]
  (area.searchArea);
);

out body;
"""

response = requests.get(overpass_url, params={'data': overpass_query})
data = response.json()

count = 0

for p in data['elements']:
    if p['id'] not in osm_id_blacklist:
        count += 1
        if 'phone' in dict(p['tags']):
            phone = p['tags']['phone']
        else:
            phone = p['tags']['contact:phone']

        print(phone.replace(" ", "").replace("+41", "0").replace("0041", "0") + " " + str(p['id']))
        #print(phone.replace(" ", "").replace("+41", "0").replace("0041", "0") + " " + str(p['id']) + " " + json.dumps(p))

print("length:", count)

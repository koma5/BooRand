import requests
import json
import time
import random

numbers = []

def get_numbers():
    global numbers
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
    if response.status_code == 200:
        numbers = []
        data = response.json()
    else:
        data['elements'] = []

    for p in data['elements']:
        if p['id'] not in osm_id_blacklist:
            if 'phone' in dict(p['tags']):
                phone = p['tags']['phone']
            else:
                phone = p['tags']['contact:phone']

            number = phone.replace(" ", "").replace("+41", "0").replace("0041", "0")
            numbers.append(number)
            #print(phone.replace(" ", "").replace("+41", "0").replace("0041", "0") + " " + str(p['id']))
            #print(phone.replace(" ", "").replace("+41", "0").replace("0041", "0") + " " + str(p['id']) + " " + json.dumps(p))

    print(len(numbers))

def gen_call_file():

    callfile_template = """
Channel: SIP/provider/{}
WaitTime: 60
Context: plaything
Extension: 1000
Priority: 1
"""
    number = random.choice(numbers)
    print(numbers)
    f = open("/callfiledrop/" + number, "x")
    f.write(callfile_template.format(number))
    f.close()


def run_times(times, sleep, function):
    count = 0
    while count < times:
        function()
        time.sleep(sleep)
        count += 1

while True:
    get_numbers()
    run_times(100, 60, gen_call_file)


from datetime import datetime

from harvest import scrape_presidential_election
from facts import states_and_dc, alloc, ev
import json

everything = {}
parties = set()

def store(result, year, state):
    if year not in everything:
        everything[year] = {}

    everything[year][state] = result

    for p in result['party']:
        parties.add(p)

for year in range(2020,1971,-4):
    for state in states_and_dc:
        store(scrape_presidential_election(state, year), year, state)

with open("output/president {}.json".format(datetime.now()), 'w') as out_file:
    out_file.write(json.dumps(everything))

print(parties)
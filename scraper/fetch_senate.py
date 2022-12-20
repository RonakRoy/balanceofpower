from datetime import datetime

from harvest import scrape_senate_elections
from facts import states, regular, special, base_years
import json

oldest_year = 1971

everything = {}
parties = set()

def store(result, year, state, seat_class):
    if year not in everything:
        everything[year] = {}

    if state not in everything[year]:
        everything[year][state] = {}

    everything[year][state][seat_class] = result

    for p in result['party']:
        parties.add(p)

for year in base_years:
    seat_class = 2 if year==2020 else (1 if year==2018 else 3)
    for state in regular[year]:
        for y, r in scrape_senate_elections(state, year, False, oldest_year, True):
            store(r, y, state, seat_class)

    for (state, seat_class) in special[year]:
        for y, r in scrape_senate_elections(state, year, True, oldest_year, True):
            store(r, y, state, seat_class)

with open("manual/senate_elections.json") as manual_file:
    manual = json.load(manual_file)

    for year in manual:
        for state in manual[year]:
            for seat_class in manual[year][state]:
                everything[year][state][seat_class]["before"] = manual[year][state][seat_class]

with open("output/senate {}.json".format(datetime.now()), 'w') as out_file:
    out_file.write(json.dumps(everything))

print(parties)

# with open("output_{}.csv".format(datetime.now()), 'w') as out_file:
#     out_file.write("state,class,")
#     for year in range(oldest_year,2021):
#         out_file.write("{},".format(year))
#     out_file.write("\n")

#     for state in states:
#         for seat_class in [1,2,3]:
#             line = "{},{},".format(state, seat_class)

#             for year in range(oldest_year,2021):
#                 results = everything[year][state].get(seat_class, None)

#                 if results != None:
#                     line += results["party"][0] + ","
#                 else:
#                     line += ","

#             out_file.write(line + "\n")
            
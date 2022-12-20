states_and_dc = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "the District of Columbia", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]

alloc = {
    "2010": [ 9,3,11,6,55,9,7,3,3,29,16,4,4,20,11,6,6,8, 8,4,10,11,16,10,6,10,3,5,6,4,14,5,29,15,3,18,7,7,20,4,9,3,11,38,6,3,13,12,5,10,3],
    "2000": [ 9,3,10,6,55,9,7,3,3,27,15,4,4,21,11,7,6,8, 9,4,10,12,17,10,6,11,3,5,5,4,15,5,31,15,3,20,7,7,21,4,8,3,11,34,5,3,13,11,5,10,3],
    "1990": [ 9,3, 8,6,54,8,8,3,3,25,13,4,4,22,12,7,6,8, 9,4,10,12,18,10,7,11,3,5,4,4,15,5,33,14,3,21,8,7,23,4,8,3,11,32,5,3,13,11,5,11,3],
    "1980": [ 9,3, 7,6,47,8,8,3,3,21,12,4,4,24,12,8,7,9,10,4,10,13,20,10,7,11,4,5,4,4,16,5,36,13,3,23,8,7,25,4,8,3,11,29,5,3,12,10,6,11,3],
    "1970": [ 9,3, 6,6,45,7,8,3,3,17,12,4,4,26,13,8,7,9,10,4,10,14,21,10,7,12,4,5,3,4,17,4,41,13,3,25,8,6,27,4,8,4,10,26,4,3,12, 9,6,11,3],
    "1960": [10,3, 5,6,40,6,8,3,3,14,12,4,4,26,13,9,7,9,10,4,10,14,21,10,7,12,4,5,3,4,17,4,43,13,4,26,8,6,29,4,8,4,11,25,4,3,12, 9,7,12,3]
}

ev = {
    2020:"2010", 2016:"2010", 2012:"2010",
    2008:"2000", 2004:"2000",
    2000:"1990", 1996:"1990", 1992:"1990",
    1988:"1980", 1984:"1980",
    1980:"1970", 1976:"1970", 1972:"1970",
    1968:"1960", 1964:"1960"
}

split_votes = {
    2008: {
        "Nebraska": {"CD2": "Democratic"}
    },
    2016: {
        "Maine": {"CD2": "Republican"}
    },
    2020: {
        "Maine": {"CD2": "Republican"},
        "Nebraska": {"CD2": "Democratic"}
    }
}

def get_total_ev(year, state):
    return alloc[ev[year]][states_and_dc.index(state)]

states = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]

classI = ["Arizona", "California", "Connecticut", "Delaware", "Florida", "Hawaii", "Indiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Jersey", "New Mexico", "New York", "North Dakota", "Ohio", "Pennsylvania", "Rhode Island", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]
classII = ["Alabama", "Alaska", "Arkansas", "Colorado", "Delaware", "Georgia", "Idaho", "Illinois", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Montana", "Nebraska", "New Hampshire", "New Jersey", "New Mexico", "North Carolina", "Oklahoma", "Oregon", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Virginia", "West Virginia", "Wyoming"]
classIII = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maryland", "Missouri", "Nevada", "New Hampshire", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "South Carolina", "South Dakota", "Utah", "Vermont", "Washington", "Wisconsin"]

regular = {
    2020: classII,
    2019: [],
    2018: classI,
    2017: [],
    2016: classIII,
    2015: []
}

special = {
    2020: [("Arizona", 3), ("Georgia", 3)],
    2019: [],
    2018: [("Minnesota", 2), ("Mississippi", 2)],
    2017: [("Alabama", 2)],
    2016: [],
    2015: []
}

base_years = [2020,2019,2018,2017,2016,2015]
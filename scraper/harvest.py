import requests
import re
import bs4
from bs4 import BeautifulSoup
from facts import states, regular, special, base_years
from facts import split_votes, get_total_ev

def make_senate_url(year, state, special=False):
    return "https://en.wikipedia.org/wiki/{}_United_States_Senate{}_election_in_{}".format(year, "_special" if special else "", state)

def make_president_url(year, state):
    return "https://en.wikipedia.org/wiki/{}_United_States_presidential_election_in_{}".format(year, state)

def print_debug(output, debug):
    if debug:
        print(output)

key_map = {
    "Image": "img",
    "Nominee": "candidate",
    "Candidate": "candidate",
    "Party": "party",
    "Percentage": "percentage",
    "Popular vote": "votes",
    "Alliance": "alliance",
    "Running mate": "running_mate",
    "Projected electoral vote": "ev",
    "Electoral vote": "ev"
}

ignored_rows = ["States carried", "Home state", "First round", "Runoff"]

def strip_citation(string):
    return re.sub(r"\[\d*\]", "", string)

def stringify(element, supstrip=True, rstrip=True, collapse=False, lower=False):
    def helper(e):
        if not e:
            return ""

        if supstrip and e.name == "sup":
            return ""
        elif e.string:
            return e.string

        string = ""
        for child in e.contents:
            if child:
                string += helper(child)

        return string
    
    string = helper(element)

    if rstrip: string = string.rstrip()
    if collapse: string = string.replace("\n", " ")
    if lower: string = string.lower()

    return string

def get_soup(url, show_output=True):
    print_debug(url,show_output)

    raw_data = requests.get(url)
    html = raw_data.content

    soup = BeautifulSoup(html, 'html.parser')

    title = soup.title.string
    year = int(title[:4])

    print_debug(title,show_output)

    return year, title, soup

def get_infobox(soup, url, year, title, state, show_output=True):
    infoboxes = soup.find_all("table", class_="infobox")

    if state in title:
        return infoboxes[0].tbody.contents

    print_debug("No individual page.",show_output)
    category = "special" if ("special" in url) else "general"
    possible_captions = [
        "{} election".format(state),                      "{} {} election".format(year,state),
        "{} {} election".format(state,category),          "{} {} {} election".format(year,state,category),
        "{} senate election".format(state),               "{} {} senate election".format(year,state),
        "{} {} senate election".format(state,category),   "{} {} {} senate election".format(year,state,category)
    ]

    for infobox in infoboxes[1:]:
        caption = stringify(infobox.caption, lower=True)
        if caption in [pc.lower() for pc in possible_captions]:
            return infobox.tbody.contents

    print_debug("Group page does not have infobox for this election.",show_output)
    return None

def get_wikitable(soup, url, year, title, state, election, show_output=True):
    wikitables = soup.find_all("table", class_="wikitable")

    category = "special" if ("special" in url) else "general"
    possible_captions = [
        "{} U.S. {} election in {}".format(year, election, state), 
        "{} U.S. {} {} election in {}".format(year, category, election, state), 

        "{} United States {} election in {}".format(year, election, state), 
        "{} United States {} {} election in {}".format(year, category, election, state),

        "{} United States {} election in {} Results".format(year, election, state), 
        "{} United States {} {} election in {} Results".format(year, category, election, state)
    ]

    # captions = []
    for table in wikitables:
        if not table.caption:
            continue

        # caption = stringify(table.caption, collapse=True, lower=True)
        # captions.append(caption)
        if stringify(table.caption, collapse=True, lower=True) in [pc.lower() for pc in possible_captions]:
            return table.tbody

    return None

def scrape_senate_elections(state, base_year, base_special=False, until_year=min(base_years), show_output=True):
    url = make_senate_url(base_year, state, base_special)

    while True:
        year, title, soup = get_soup(url, show_output)

        infobox = get_infobox(soup, url, year, title, state, show_output)
        wikitable = get_wikitable(soup, url, year, title, state, "Senate", show_output)
        
        if infobox:
            results, prev_year, prev_url = scrape_infobox(year, title, infobox, show_output)

            try:
                before = infobox[len(infobox)-1].td.table.tbody.tr.find_all("td")[0].p.find_all("a")
                before_senator = before[0].string
                before_party = before[1].string

                results["before"] = { "senator": before_senator, "party": before_party }
            except:
                print_debug("Incumbent unknown.",show_output)
        elif wikitable:
            results = scrape_wikitable(year, title, wikitable, show_output)
            prev_year, prev_url = (None,None)
        else:
            print("SCREEEEE")

        results["special"] = "special" in url
        yield year, results

        if not prev_year:
            break
        elif prev_year < until_year:
            break
        url = prev_url

def scrape_presidential_election(state, year, show_output=True):
    url = "https://en.wikipedia.org/wiki/{}_United_States_presidential_election_in_{}".format(year, "Washington (state)" if state == "Washington" else state)

    year, title, soup = get_soup(url, show_output)

    infobox = get_infobox(soup, url, year, title, state, show_output)
    wikitable = get_wikitable(soup, url, year, title, state, "presidential", show_output)

    results, _, _ = scrape_infobox(year, title, infobox, show_output)

    results["total_ev"] = get_total_ev(year, state)

    if year in split_votes:
        if state in split_votes[year]:
            results["split"] = split_votes[year][state]

    return results


def scrape_infobox(year, title, infobox, show_output=True):
    for i in range(2,len(infobox)):
        try:
            race_info = infobox[i].td.table.tbody.find_all("tr")
            break
        except:
            pass

    results = {}
    for row in race_info:
        cells = []

        if not row.find("th"):
            row_name = "Image"
            for cell in row.find_all("td"):
                img = cell.find("img")
                if img: cells.append("http:" + img["src"])
        else:
            row_name = stringify(row.find("th")).replace(u'\xa0', u' ')
            for cell in row.find_all("td"):
                string = stringify(cell)
                if string != "": cells.append(string)

        if row_name in ignored_rows: continue
        key = key_map[row_name]
        results[key] = results.get(key,[]) + cells

    for key in results:
        if key == "img":
            continue

        line = ""
        for col in results[key]:
            line += "{:>30} ".format(col)
        print_debug(line, show_output)

    print_debug("",show_output)
    
    try:
        prev_election = infobox[1].td.table.tbody.tr.td.a["href"]
    except:
        prev_election = infobox[1].td.div.div.a["href"]
    try:
        prev_year = int(prev_election[6:10])
    except:
        prev_year = int(prev_election[-4:])

    return results, prev_year, "http://en.wikipedia.org" + prev_election

def scrape_wikitable(year, title, wikitable, show_output=True):
    candidates = wikitable.find_all('tr', class_="vcard")
    party_change = stringify(wikitable.find_all('tr')[-1].find_all('td')[1])

    results = {"img":[], "candidate":[], "party":[], "votes":[], "percentage":[], "before":{}}
    for candidate in candidates:
        columns = candidate.find_all('td')

        name = stringify(columns[2])
        if "Incumbent" in name:
            name = name.replace(" (Incumbent)","")
            results["before"]["senator"] = name
        results["candidate"].append(name)

        results["img"].append(stringify(""))
        results["party"].append(stringify(columns[1]))
        results["votes"].append(stringify(columns[3]))
        results["percentage"].append(stringify(columns[4]))

    if "gain from" in party_change:
        results["before"]["party"] = party_change.split(" gain from ")[1]
    else:
        results["before"]["party"] = party_change.split(" hold")[0]

    return results

if __name__ == "__main__":
    for e in scrape_senate_elections("Alaska", 2016, False, 2016, True):
        print(e)
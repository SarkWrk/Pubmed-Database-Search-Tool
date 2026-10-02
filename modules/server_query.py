import os
from os import path
import json
import requests
import time
import xml.etree.ElementTree as ET


# Dirname
dirname = os.path.dirname(os.path.dirname(__file__))

# Dictionary of queries
queries = {}
settings = {}

# Paths
output_path = ""
log_level = ""

with open(path.join(path.join(dirname, "settings"), "queries.json"), "r", encoding="UTF-8") as queries_file:
    queries = json.loads(queries_file.read())

with open(path.join(path.join(dirname, "settings"), "settings.json"), "r", encoding="UTF-8") as settings_file:
    settings = json.loads(settings_file.read())
    output_path = settings["paths"]["input"]
    log_level = settings["log_level"]

# Set up query templates
db = queries["db"]
eutil_base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
eutil_search_url = "esearch.fcgi?db={}&term=".format(db)
eutil_fetch_url = "efetch.fcgi?db={}".format(db)

rettype = "abstract"
retmax = queries["max_retrievals_per_get"]

# Query the server for UIDs
xml_output = {}
for query in queries["new_queries"]:
    print("Querying: \"{}\"".format(query))

    modified_query = query.replace(" ", "+")
    new_search = "{}{}{}&usehistory=y".format(eutil_base_url, eutil_search_url, modified_query)

    output = None

    try:
        output = requests.get(new_search)
    except requests.RequestException as e:
        if log_level == "Errors" or log_level == "Debug":
            print("An error occurred when querying: \"{}\"".format(query))
        if log_level == "Debug":
            print(e)
        continue


    xml_output[query] = output.text
    
    # Caution over the 3 queries per second limit
    time.sleep(0.5)

# Obtain the abstracts for each query
for content in xml_output:
    tree = ET.fromstring(xml_output[content])
    web_env = tree.find("WebEnv").text
    query_key = tree.find("QueryKey").text
    count = tree.find("Count").text

    data_list = []

    print("Retrieving abstracts for query: \"{}\"".format(content))

    for i in range(0, int(count), retmax):
        if log_level == "Debug":
            print("Querying at {} for query \"{}\"".format(i, content))

        new_fetch = """{}{}&WebEnv={}&query_key={}&retstart={}&retmax={}&rettype={}&retmode=text""".format(eutil_base_url, eutil_fetch_url, web_env, query_key, i, retmax, rettype)

        output = None

        try:
            output = requests.get(new_fetch)
        except requests.RequestException as e:
            if log_level == "Errors" or log_level == "Debug":
                print("An error occurred when obtaining abstracts for: \"{}\"\nAbstracts from indexes {} to {} will be skipped...".format(content, i, i + retmax))
            if log_level == "Debug":
                print(e)
            continue

        data_list.append(output.text)

        # Caution over the 3 queries per second limit
        time.sleep(0.5)
    
    output_text = ""
    
    for data in data_list:
        output_text = output_text + data + "\n"
    
    data_hash = hash(output_text)

    with open(path.join(path.join(dirname, output_path), "{}.txt".format(data_hash)), "w+", encoding="UTF-8") as output_file:
        if log_level == "Debug":
            print("Writing to file")

        output_file.write(output_text)
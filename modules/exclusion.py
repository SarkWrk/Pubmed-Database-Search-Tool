import os
import json
import datetime
import re as regex

# Remove duplicates
import modules.duplicate_remover

# Relative paths for file locations
input_path = ""
output_path = ""

# Filter terms
terms_1_list = [] # This is regex
terms_2_list = [] # This is regex

# This is used to title the output .csv file
dt = datetime.datetime.now()

# Estimated read time params
words_per_min = 120
characters_per_word = 5

# List of articles to be put in the output .csv file
accepted_articles = {}

# Character count stuff for estimate
total_characters = 0

# Dirname
correct_dir = os.path.dirname(os.path.dirname(__file__))

# Log level
log_level = ""

with open(os.path.join(os.path.join(correct_dir, "settings"), "settings.json"), "r") as settings_file:
    settings_string = settings_file.read()
    settings = json.loads(settings_string)
    
    input_path = settings["paths"]["output"]
    output_path = settings["paths"]["wanted"]

    log_level = settings["log_level"]

    exclusion_criteria = settings["exclusion_criteria"]

    for criteria in exclusion_criteria["terms_1"]:
        terms_1_list.append(criteria.replace("\\\\", "\\"))

    for criteria in exclusion_criteria["terms_2"]:
        terms_2_list.append(criteria.replace("\\\\", "\\"))

with open(os.path.join(os.path.join(correct_dir, input_path), "export.json"), 'r', encoding="UTF-8") as input_file:
    lines = json.loads(input_file.read())
    abstract_index = 3
    
    for line in lines:
        data = lines[line]
        
        # Clean the authors field of (n)
        data["Authors"] = regex.sub(r"\(\d+\)", "", data["Authors"])

        abstract = data["Abstract"]
        pmid = data["PMID"]

        # Article filtering starts here

        passed_term_1_check = False
        passed_term_2_check = False

        for re in terms_1_list:
            found_in = regex.findall(" " + re + " ", abstract.casefold())
            if found_in:
                passed_term_1_check = True

        if passed_term_1_check == False:
            continue

        for re in terms_2_list:
            found_in = regex.findall(" " + re + " ", abstract.casefold())
            if found_in:
                passed_term_2_check = True

        if passed_term_2_check == False:
            continue

        # Article filtering ends here

        # Add to dictionary and character count for estimate
        accepted_articles[pmid] = data
        total_characters += len(abstract)
    
# Write to file
with open(os.path.join(os.path.join(correct_dir, output_path), str(dt.year) + "-" + str(dt.month) + "-" + str(dt.day) + ".json"), "w+", encoding="UTF-8") as output_file:
    output_string = json.dumps(accepted_articles, indent=4, ensure_ascii=False, sort_keys=True)
    output_file.write(output_string)

print("Estimated: {}min".format(round(total_characters/(words_per_min*characters_per_word))))
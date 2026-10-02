> [!NOTE]
>
> This programme uses E-Utilities. You can find NCBI's disclaimer and copyright notice here: [https://www.ncbi.nlm.nih.gov/home/about/policies/](<https://www.ncbi.nlm.nih.gov/home/about/policies/>).

*To use the programme:*

1. Install the `requests` module.
2. Add your search queries in ./settings/queries.json. (Change databases by modifying "db" and change the amount of abstracts retrieved per query by modifying "max_retrievals_per_get".)
3. Change the regex strings in 'exclusion_criteria' in ./settings/setings.json to the values you want. (Optionally, change the code for the article filtering in ./modules/exclusion.py to fit your needs)
4. Run main.py.
5. Results are in ./wanted/{YYYY-MM-DD}.json.

***
*Programme information:*

Files in ./out are parsed versions of the text files (of the same name) in ./in which were converted to a json friendly format.

Log levels are as followed:
- "None" (only normal status logging)
- "Errors" (information if the code errors)
- "Debug" (more logging, supersedes "Errors")

```
| ...
|-main.py                   # Runs each file in ./modules in the correct order
|-modules/
    /-duplicate_remover.py  # Removes duplicate articles and combines all unique articles into ./out/export.json
    /-exclusion.py          # Uses regex to exclude unwanted articles from ./out/export.json; the unexcluded articles will be put in ./wanted/{YYYY-MM-DD}.json
    /-formatter.py          # Parses each text file created from ./modules/server_query.py and creates a json formatted version of the file in ./out with the same name
    /-server_query.py       # Queries E-Utilities to obtain abstracts from PubMed and puts the results in ./in (with the hash of the text output as its name)
|-settings/
    /-queries.json          # Query settings/parameters go here
    /-settings.json         # File used for various information (e.g. paths, logging level, regex used in ./modules/exclusion.py)
| ...
```

***

This project is licensed under the MIT License.


# Scraping Projects


## 1) [GOAL] Improving Scrapers 
**Related Files**

- Current Scrapers
```
    AC_Current_Scrapers\ ## See Project Brief for more info on acronym meaning. 
            adb_spf_scraper.py
            afdb_scraper.py
            cao_scraper.py
            eib_scraper.py
            ebrd_pcm_scraper.py
            mici_scraper.py
            panel_scraper.py
            eib_project_scraper.py (lower priority)
```
This folder also contains outputs of these scrapers for reference. 

- Template Scraper
```
    Template_Scraper\
        mici-scraper.py # Template scraper using Requests & BS4
        Selenium-beautifulsoup-example.ipynb # Template Selenium BS4 example
```

### a) Making the scrapers (both kinds) more robust and less prone to break 
Additional IAM web scrapers (Panel, IAB, MICI, EIB, CAO). DataKind will work with DataDive support volunteers to identify guidelines for improvement. Also see `/Ref/Common Scraper Issues.txt`.


Major areas for improvement include
* More resilient to minor changes in website structure
* Run faster 

    **Template Scraper**
    
    ```
    Template_Scraper\
       mici-scraper.ipynb
    ```

#### strategy for a new scraper
    * have a common set of fields (common model) for all the scrapers [Master scraper]
    * store the list of projects as dataframe
    * export the result to a CSV

#### strategy to combine all CSVs
    * collate all CSVs to one CSV in a local folder with timestamp to avoid overriding

### b) Updating the scrapers to include downloading documents (e.g. PDFs) and storing them. 
* A sub team at the DataDive can work on building a code “module” that can be added to search for linked documents and download them to a generic destination.
* Destination would likely be a DataKind s3 bucket with a container labeled by project ID, for even it would be fine if just pulled docs into a folder labeled by {{scraper label}}{{project id|or|Title+ProjectDate}}

### c) Potential additional goals (Stretch Goals) - subject to further review:
* Develop code to automate the running of this scrapes, AC would love to just see a few examples of how this could be done. So even a couple of different solutions could allow the understand what solution works best for them, some initial requirements:
    * Easy to edit timing of scrape execution
    * Asynchronous
    * Resilient to errors in one of the scrapes (completes other scrape runs even if one errors out)


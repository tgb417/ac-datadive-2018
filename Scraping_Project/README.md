

# Scraping Projects


## 1) [GOAL] Improving Scrapers 
**Related Files**
```
    AC_Current_Scrapers\ ## See Project Brief for more info on acronym meaning. 
            adb_spf_scraper.py
            panel_scraper.py
            cao_scraper.py
            eib_scraper.py
            mici_scraper.py
            panel_scraper.py
            eib_project_scraper.py (lower priority)
```

**Template Scraper**
```
    Notebooks\
        DK_ScraperReview.pynb : Just the scraper code copied 
            into a notebook for review purposes. 
        Complaint_Data_Scraped_Review.ipynb: Mostly empty 
            notebook where we quickly reviewed the scraped data file.
```

### a) Making the scrapers (both kinds) more robust and less prone to break 
Additional IAM web scrapers (Panel, IAB, MICI, EIB, CAO). DataKind will work with DataDive support volunteers to identify guidelines for improvement. Also see `/Ref/Common Scraper Issues.txt`.


Major areas for improvement include
* More resilient to minor changes in website structure
* Run faster 

### b) Save and Compare Scrapes [FILL ME IN PLEASE]
* Code to compare older web scrape to a newer web scrape (old scrape data in /Data/Complaint_Data_Scraped.xlsx)
* DK will save a complete scrape list (Data/Complaint_Data_Scraped.xlsx)
DK / AC will create a test set of “changed” scrape examples (Need to support AC in creating this)
* Write code to save the new scrapes  (THIS MAY NOT MAKE SENSE HERE - may not be a DD goal - just something with can help AC implement on the side)
* Develop code to automatically flag changes in new scrapes to previous scrapes and provide output for AC review. (Need to create "fake" changed scrape data - a sample of rows from Data/Complaint_Data_Scraped.xlsx where minor changes have been made.)
* Output --> Simple text table indicating the project number and fields that have changed in the scraped data. 

### c) Updating the scrapers to include downloading documents (e.g. PDFs) and storing them. 
* A sub team at the DataDive can work on building a code “module” that can be added to search for linked documents and download them to a generic destination.
* Destination would likely be a DataKind s3 bucket with a container labeled by project ID, for even it would be fine if just pulled docs into a folder labeled by {{scraper label}}{{project id}}

### d) Potential additional goals (Stretch Goals) - subject to further review:
* Develop code to automate the running of this scrapes, AC would love to just see a few examples of how this could be done. So even a couple of different solutions could allow the understand what solution works best for them, some initial requirements:
    * Easy to edit timing of scrape execution
    * Asynchronous
    * Resilient to errors in one of the scrapes (completes other scrape runs even if one errors out)
* (UNLIKELY GOAL) Create additional scrapers for the sites listed in this link which have not been written yet.

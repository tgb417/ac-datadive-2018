

# Compare Scrapes


## a)  Compare Scrapes 
* Code to compare older web scrape to a newer web scrape 
* Develop code to automatically flag changes in new scrapes to previous scrapes and provide output for AC review. 
* Output --> Simple text table indicating the project number and fields that have changed in the scraped data. 

    **Diff Analysis**
    ```
    Diff_Analysis\
       Complaint_Data_Scraped.xlsx
       Complaint_Data_Scraped_diff.xlsx
       example_output.xlsx
    ```

## b)  Requirements
* Must work with any results file
* Column name agnostic
* Records summary of changes

## c) Data Summary
`Complaint_Data_Scraped.xlsx` contains the output of the existing scrapers, while `Complaint_Data_Scraped_diff.xlsx` is the same output with a subset of columns in 4 of the 5 sheets permuted. The code used to produce the second file is saved in `../_Admin/Setup/Notebooks/diff_data.ipynb`. The altered columns in each sheet are
* Panel - 'Filing Date', 'Date Closed'
* EIB - 'Dispute Resolution End Date', 'Documents'
* MICI - 'Compliance Review Start Date', 'Date Closed'
* CAO - 'Monitoring Start Date', 'Monitoring End Date'
* ADB - No changes

    

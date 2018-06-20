# Complaint Analysis


## 2) [GOAL] Understanding Complaint Ineligibility  
**Related Data** 
* data/accountability_console_2018-02-24.csv - Complaint Data
* data/ac_benchmarks_data_2018-05-11.csv - Data related to the how the different banks handle complaints, and other info. (like bank metadata)

**Scoping Notebooks**
```
    Notebooks\
        DK_Exploration_MDowd.ipynb: Some simple EDA of the Complaint and Benchmark(Bank realated) data. 
```

**Goals**
* Clean and parse data for exploratory analysis
* Identify features that have reasonable completeness
etc.
* Describe Data 
* Featurize data
* Transformation of 30+ other variables related to each complaint into numerical or categorical features. 
* Exploring reasons listed for ineligibility and generating summary statistics (60+ unique reasons across all complaints, although some have more than one reason listed.) 
* Complaint features used for correlations and downstream modeling are usable (i.e. Is this information effectively known ahead of filing a complaint?) 
* Categorizing 60+ “No Eligibility” unique reasons into smaller categories to support downstream modeling (AC may be working on this internally - need to check in with them)
* Develop meaningful visualizations 
* Attempt to answer the questions
    * What are the top commonalities across complaints that are deemed ineligible?” 
    * What trends or patterns can be seen by exploring the data on complaints and ineligibility.
    * “What are the biggest factors driving ineligibility?” with a model that balances accuracy with minimal overfitting. 
    * What impact do IAM characteristics have on eligibility outcomes (benchmark data)
    * ...
* Develop Code and visualizations that can be handed over and understood by Accountability Counsel team 
* Correlation study/univariate analysis between eligibility and the ~30 columns of metadata available (including transformations of the variables) 
* Predicting eligibility via supervised modeling (if the data supports it.)  e.g. Logistic regression, decision tree. 



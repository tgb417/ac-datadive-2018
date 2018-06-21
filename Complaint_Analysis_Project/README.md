
# Complaint Analysis


## 2) [GOAL] Understanding Complaint Ineligibility  





## Introduction 

Welcome to the DataDive, and thank you for volunteering! If you are reading this, then you are likely interested in participating the analytics subgroup of the Accountability Counsel (AC) project. The purpose of this document is to introduce you to the data you'll be using, take you through some of its features and peculiarities, and list some analysis questions suggested to us by the Accountability Counsel. It is meant to help you get started with your analysis, but is not comprehensive - so if you are confused by anything, or find yourself pondering a question that this document doesn't answer, please ask me! I (Emily) will be with you all weekend, and my job is to make it easier for you derive as much insight from the data as you can.

## Overview of the Data

For a more detailed overview of this project, and of the Accountability Counsel in general, please see the project brief here:  https://tinyurl.com/ac-projectbrief 

The link to the AC website is here: https://www.accountabilitycounsel.org/

You will be working with two datasets this weekend. They are as follows: 

### `accountability_console_data_cleaned.csv`

The first is a cleaned up version of the complaint data that can be exported from the AC's web console. At its lowest level, it contains information pertaining to complaints submitted to, and monitored by, AC. A single record of this data corresponds to an individual complaint. The data also contains information about the countries involved, the industries/sectors tied to the complaint, categories (issues) for the complaints, the independent accountability mechanisms (IAMs) investigating the complaints, as well as various dates surrounding complaint eligibility, dispute resolution, compliance reports, and monitoring. For an overview of the steps involved with/life cycle of a complaint, please see the project brief.

The complaint data can be found in either `accountability_console_data_cleaned.csv`, or, if you are an R user, I have also exported the data as an RData file in `accountability_console_data_cleaned.RData`.

### `benchmark_data_cleaned.csv`

The second dataset you'll be working with contains benchmark data - basically, qualifying information regarding complaint procedures - for the top 8 IAMs. This data is very simple; it consists of benchmark categories, individual benchmark questions (mostly yes/no, but there are a few questions pertaining to timeframes of certain aspects of the complaints), and their answers - there is a column for each IAM's answer. An individual record corresponds to a single benchmark question.  

The benchmark data can be found in `benchmark_data_cleaned.csv` and `benchmark_data_cleaned.RData`. Melted data (in which a record corresponds to an individual IAM's answer to a single benchmark question) can be found in `benchmark_data_cleaned_melted.csv` and `benchmark_data_cleaned_melted.RData`. Use whichever format you'd like in your analysis.


## Questions for Analysis

The great thing about this part of the project is that it's tool-agnostic - whether your analysis tool of choice is R, Python, SAS, Excel, Tableau, or anything in between - use whatever you're most comfortable with to work on the data. 

Here is a list of questions into which AC is hoping to gain insight using the complaints and benchmark data:

* Describe data, both complaints and benchmarks
* Featurize data, both complaints and benchmarks
* Exploring reasons listed for ineligibility and generate summary statistics -- try to identify common properties of complaints that are rendered ineligible by the mechanism
* Determine if complaint features used for correlations and downstream modeling are usable (i.e. Is this information effectively known ahead of filing a complaint?) 
* Develop meaningful visualizations of both datasets
* Attempt to answer the question: What trends or patterns can be seen by exploring the data on complaints and ineligibility?
* If possible: What are the biggest factors driving ineligibility? Try to develop a model that balances accuracy with minimal overfitting. 
* Correlation study/univariate analysis between eligibility and the ~30 columns of metadata available (including transformations of the variables) 
* Predicting eligibility via supervised modeling -- if the data supports it, e.g. Logistic regression, decision tree. Does the data support this?

Additionally, AC is keenly interested in finding out whether or not the answers to specific benchmark questions have any bearing on complaint eligibility. They are:

* Is the CR conducted by the mechanism staff, independent experts/panelists, or both?
* Does the mechanism have the independent authority to accept and conduct CR?
* If CR [compliance review] is sought, must PS [problem solving] occur first?
* Does the policy contain restrictions concerning past or ongoing judicial, arbitral, or administrative proceedings?
* Does the policy contain restrictions concerning past or ongoing IAM proceedings?          
* May the mechanism conduct compliance review for completed projects?
* May the mechanism conduct problem solving for completed projects?
* May a claim be brought after full disbursal of funds?
* May a claim be brought after physical completion of the project?"
* May a claim be brought before a project is approved by the institution's Board?
* May claimants make comments on draft findings?
* Are draft findings made available to claimant?
* Must management prepare an action plan in consultation with requestors? 

## Some Questions to Get You Started

Think of this section as warm-up exercises to consider as you dig in to the data. If you're comfortable diving right in, then by all means, do so! However, if you're not sure where to begin, try your hand at some of these questions. They are meant to help you ensure that you've successfully loaded the data and will help you familiarize yourself with some of the columns. 

* Which country/region is represented most often in the complaints data?
* Which IAM has investigated the most complaints?
* Which issue is least represented in the complaints data?
* Which IAM found the highest rate of noncompliance?
* Consider the benchmark question "How long does the mechanism take to determine eligibility for further review?" Which IAM has the longest turnaround time?
* Which IAM answers "Yes" to the most Transparency questions? Which one is the least transparent?
* What is the longest period, in days, for which a (closed) complaint was active?

## What to Do with Your Work

Throughout the weekend, as you come up with insights, visualizations, or anything you find to be interesting about the data, please upload them to the [Project Page](https://docs.google.com/document/d/1cOjGz7mkF945cgqEgjbj6i8lIAkadGwmj1FBwj94awc/edit#) and [Slack](https://tinyurl.com/AC-slack). 

Also **PLEASE** upload all code to the [AC Drive](https://tinyurl.com/ac-DDmaterials),  AC is interested in reproducing this work, so the easier we can make it for them, the better!

I will be checking in with you periodically throughout the day to get updates on your findings and provide assistance if needed. Please do not hesitate to ask if you have any questions.

Thanks again, and happy exploring!






## Details: Complaints Data

In this section, I provide an overview of the columns in the complaints file and some things to look out for as you work with the data.

* `Complaint_Name` and `Project` will often be identical, or at least very similar. There are `r n_distinct(complaints$Project)` distinct projects and `r n_distinct(complaints$Complaint_Name)` distinct complaint names. In two cases, complaints seem to have the same name - if you need to reference either of these cases, be sure to include the `External_ID` as well (there are `r nrow(complaints)` unique combinations of `Complaint_Name` and `External_ID` - so this would be the "primary key" for the dataset.)
* `Country_1`, `Country_2`, `Country_3`, `Country_4` : In the original raw data set, there was one `Country` column representing the countries/regions affected by proposed developments, but this column often contained multiple comma-separated values. The highest country count associated with any single complaint is four, so I split this column up. When analyzing the countries tied to complaints, be sure to include the values in all of these columns.
* `IAM` represents the Independent Accountability Mechanism investigating the complaint. A list of all 14 IAMs can be found in the project brief. 
* `Bank` represents the financial institution tied to the complaint. There are 14 of these (each has its own IAM.)
* The `Status` column represents the status of the complaint. Note that a status of "Closed With Results" is distinct from a status of "Closed With Results Outside Process" - the latter often signifies that the complaintants resolved their issues outside of the IAM process. 
* The `Filer` column contains the names of individuals/organizations who are filing complaints. This column is often null, and there can be many filers tied to a single complaint, so I did not bother splitting this column up into several. Individual complaintants will likely not have any bearing on your analysis.
* `IFI_Support_1`, `IFI_Support_2` : IFI stands for International Finance Institution. These columns represent the servives provided by the banks. Nearly always, only `IFI_Support_1` will be populated, but bear in mind that sometimes `IFI_Support_2` will have a value.
* `Sector_1`, `Sector_2`, `Sector_3` stand for the different industries represented by the complaints. Only one complaint will have more than two.
* `Issue_1`, `Issue_2`, ... , `Issue_10` : A complaint can have up to 10 issues tied to it, such as "Due diligence," "pollution," "Other community health and safety issue," etc.
* `Description` : This column is almost always unpopulated, and can be excluded from any analysis.
* `Compliance_Report_Issued`, `Noncompliance_Found` : This true/false column is almost always populated, with ~10% of values being "true."
* `Filing_Date` is the date the complaint was filed, and is almost completely populated. Dates go back to 1994.
* `Registration_Start`, `Registration_End`, `Registration_Status`, `If_No_Registration_Why` : represents the date the complaint was registered [to what?] Some IAMs (ABD_SPF_CRP in particular) nearly always have a registration date as well as a filing date; others do not (IFC_CAO, for example, does not have registration date data for any of its 260 complaints.)
* `Eligibility_Start`, `Eligibility_End`, `Eligibility_Status`, `If_No_Eligibility_Why_1`, ... `If_No_Eligibility_Why_3` : AC is particularly interested in analysis surrounding complaint eligibility. `Eligibility_Date`, as the name implies, contains the date a complaint was found to be elibile for action by the IAM. If a complaint is not found to be eligible, then it will have a reason listed in up to 4 of the `If_No_Eligibility_Why` columns. However, in a significant number of cases (about 282/815) a complaint will have no eligibility date, but no reason listed - look to the next columns to try and determine why. Sometimes this is because a complaint was immediately deemed ineligible at the outset and thus never went through the complaint mechanism. `Eligibility_Status` gives the explicit state of a complaint.
* `Dispute_Resolution_Start`, `Dispute_Resolution_End`, `Dispute_Resolution_Status`, `If_No_Dispute_Resolution_Why` : These columns contain dates for dispute resolution periods if a complaint entered one. However, `Dispute_Resolution_Status` almost always has a value even if a complaint did not enter a dispute. Most of the time, this status will be "Not Undertaken," but there are a few cases that don't have this status. `Dispute_Resolution_Start` and `Dispute_Resolution_End` mark the beginning and end dates of dispute resolution, if a complaint went through this stage.
* `Compliance_Review_Start`, `Compliance_Review_End`, `Compliance_Review_Status`, `If_No_Compliance_Report_Why` : Generally, complaints go through either dispute resolution or compliance review, with the respective outcome of a mutual agreement between parties or a full compliance report. However, sometimes the dispute resolution stage fails to successfully resolve the dispute, so at this point the complaint will enter the compliance review stage. Complaints can progress from dispute resolution to compliance review, but the mechanism does not allow the reverse to occur. 
* `Monitoring_Start`, `Monitoring_End`, `Monitoring_Status`, `If_No_Monitoring_Why` :
* `Date_Closed` : The date the complaint was closed by its IAM. Note that some cases are still in progress, so not every complaint will have a close date. Additionally, a complaint can be functionally "closed" for the purpose of its IAM, but remain in a "monitoring" phase for up to three years - this should explain the complaints whose statuses are similar to "Closed" but don't have a value in the `Date_Closed` column.

## Details: Benchmarks Data

* `Category` : Every benchmark question is assigned to a category - there are 33 categories in total. This column should not ever be null.
* `Benchmark` : As stated earlier, a benchmark is question whose answer provides qualifying information regarding the IAM investigating a claim. Most of these questions are yes/no, or their answers involve lengths of time. A few involve stating decision makers during key steps in the complaint process. Where lengths of time are concerned, I have converted all measurements to days.
* `AfDB_IRM`, `ADB_SPF_CRP`, `EBRD_PCM`, `EIB_CM`, `IFC_CAO"IDB_MICI`, `OPIC_OA`, `WB_Panel` : The rest of the columns correspond to individual IAMs and their answers to the benchmark questions. Note that only 8 of the 14 IAMs are represented in this dataset. 




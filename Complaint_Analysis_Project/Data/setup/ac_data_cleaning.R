library(reshape2)
library(lubridate)
library(dplyr)
library(tidyr)
library(stringr)

# Loading in raw data
benchmarks <-
  read.csv(
    "~/repos/DataKind/ac-datadive-2018/Complaint_Analysis_Project/Data/raw/ac_benchmarks_data_2018-06-20.csv",
    header = TRUE,
    sep = ",",
    stringsAsFactors = FALSE
  )
complaints <-
  read.csv(
    "~/repos/DataKind/ac-datadive-2018/Complaint_Analysis_Project/Data/raw/accountability_console_2018-06-18.csv",
    header = TRUE,
    sep = ",",
    stringsAsFactors = FALSE
  )

# Renaming variables (I hate periods in variable names) and fixing data types
colnames_complaints <-
  c(
    "Complaint_Name",
    "Project",
    "Country",
    "IAM",
    "Bank",
    "External_ID",
    "Status",
    "Filer",
    "IFI_Support", #
    "Sector",
    "Issues",
    "Description",
    "Compliance_Report_Issued", #
    "Noncompliance_Found",
    "Filing_Date",
    "Registration_Start",
    "Registration_End",
    "Registration_Status",
    "If_No_Registration_Why", #
    "Eligibility_Start",
    "Eligibility_End",
    "Eligibility_Status",
    "If_No_Eligibility_Why",
    "Dispute_Resolution_Start",
    "Dispute_Resolution_End",
    "Dispute_Resolution_Status",
    "If_No_Dispute_Resolution_Why", #
    "Compliance_Review_Start",
    "Compliance_Review_End",
    "Compliance_Review_Status",
    "If_No_Compliance_Report_Why", #
    "Monitoring_Start",
    "Monitoring_End",
    "Monitoring_Status",
    "If_No_Monitoring_Why",
    "Date_Closed"
  )
names(complaints) <- colnames_complaints

colnames_benchmarks <- c(
 "Category",
 "Benchmark",
 "AfDB_IRM",
 "ADB_SPF_CRP",
 "EBRD_PCM",
 "EIB_CM",
 "IFC_CAO",
 "IDB_MICI",
 "OPIC_OA",
 "WB_Panel"
  )
names(benchmarks) <- colnames_benchmarks

# No nulls? Then probably nulls are all empty strings... let's see
for (i in seq_along(names(complaints))){
  print(paste0("The column ", names(complaints[i]), " contains ", sum(complaints[i] == "")," values that are empty strings."))
} 
for (i in seq_along(names(benchmarks))){
  print(paste0("The column ", names(benchmarks[i]), " contains ", sum(benchmarks[i] == "")," values that are empty strings."))
}

# Lots of empty strings in the complaints data; not so much in the benchmark data. But we'll change both anyway
for (i in seq_along(names(complaints))){
  complaints[i][which(complaints[i] == ""),] <- NA  
}
for (i in seq_along(names(benchmarks))){
  complaints[i][which(benchmarks[i] == ""),] <- NA  
}

## Now honing in on the complaints data...

# Reformatting the dates in the complaints data
complaints$Filing_Date <- date(as.POSIXct(complaints$Filing_Date, format = "%m/%d/%y"))
complaints$Registration_Start <- date(as.POSIXct(complaints$Registration_Start, format = "%m/%d/%y"))
complaints$Registration_End <- date(as.POSIXct(complaints$Registration_End, format = "%m/%d/%y"))
complaints$Eligibility_Start <- date(as.POSIXct(complaints$Eligibility_Start, format = "%m/%d/%y"))
complaints$Eligibility_End <- date(as.POSIXct(complaints$Eligibility_End, format = "%m/%d/%y"))
complaints$Dispute_Resolution_Start <- date(as.POSIXct(complaints$Dispute_Resolution_Start, format = "%m/%d/%y"))
complaints$Dispute_Resolution_End <- date(as.POSIXct(complaints$Dispute_Resolution_End, format = "%m/%d/%y"))
complaints$Compliance_Review_Start <- date(as.POSIXct(complaints$Compliance_Review_Start, format = "%m/%d/%y"))
complaints$Compliance_Review_End <- date(as.POSIXct(complaints$Compliance_Review_End, format = "%m/%d/%y"))
complaints$Monitoring_Start <- date(as.POSIXct(complaints$Monitoring_Start, format = "%m/%d/%y"))
complaints$Monitoring_End <- date(as.POSIXct(complaints$Monitoring_End, format = "%m/%d/%y"))
complaints$Date_Closed <- date(as.POSIXct(complaints$Date_Closed, format = "%m/%d/%y"))

# Renaming complaints IAM values to match the Benchmarks headers
print(unique(complaints$IAM))
complaints$IAM[which(complaints$IAM == "ADB Special Project Facilitator and Compliance Review Panel")] <- "ABD_SPF_CRP"
complaints$IAM[which(complaints$IAM == "EIB Complaints Mechanism")] <- "EIB_CM"
complaints$IAM[which(complaints$IAM == "IFC Compliance Advisor/Ombudsman")] <- "IFC_CAO"
complaints$IAM[which(complaints$IAM == "IDB Independent Consultation and Investigation Mechanism")] <- "IDB_MICI"
complaints$IAM[which(complaints$IAM == "EBRD Project Complaint Mechanism")] <- "ERBD_PCM"
complaints$IAM[which(complaints$IAM == "WB Inspection Panel")] <- "WB_Panel"
complaints$IAM[which(complaints$IAM == "EBRD Independent Resource Mechanism")] <- "ERBD_IRM"
complaints$IAM[which(complaints$IAM == "OPIC Office of Accountability")] <- "OPIC_OA"
complaints$IAM[which(complaints$IAM == "AfDB Independent Review Mechanism")] <- "AfDB_IRM"
complaints$IAM[which(complaints$IAM == "JBIC Examiner for Environmental Guidelines")] <- "JBIC_EEG"
complaints$IAM[which(complaints$IAM == "COES Corporate Social Responsibility Counsellor")] <- "COES_CSR"
complaints$IAM[which(complaints$IAM == "JICA Examiner for Environmental Guidelines")] <- "JICA_EEG"
complaints$IAM[which(complaints$IAM == "UNDP Social and Environmental Compliance Unit")] <- "UNDP_SRM"
complaints$IAM[which(complaints$IAM == "FMO Independent Complaints Mechanism")] <- "FMO_ICM"

# Cleaning up complaint country names
print(sort(unique(complaints$Country))) # Looks like a few entries have comma separated lists
length(grep(",", complaints$Country)) # Total is 9; the most countries attached to a complaint is 4
complaints$Country <- ifelse(complaints$Country == "Unknown", NA, complaints$Country)
complaints <- complaints %>%
  separate(Country, c("Country_1", "Country_2", "Country_3", "Country_4"), ",")

# Banks
unique(complaints$Bank) # These are good - don't need to be cleaned

# External_ID did not need cleaning

# Cleaning up complaint status data
unique(complaints$Status) # 6 unique vales - cleaning now needed

# Cleaning up complaint filer data
unique(complaints$Filer) # NA and AC... not much to do with this column.
sum(complaints$Filer == "Unknown" | is.na(complaints$Filer)) # Over half unknown or null
complaints$Filer[which(complaints$Filer == "Unknown")] <- NA

# Cleaning up complaint IFI support data
unique(complaints$IFI_Support) # Only 13, that's cool
sum(complaints$IFI_Support == "No IFI involvement" | is.na(complaints$IFI_Support))
complaints$IFI_Support[which(complaints$IFI_Support == "No IFI involvement")] <- NA
  # There are some comma-separated values again, but I think they can be split up
complaints <- complaints %>%
  separate(IFI_Support, c("IFI_Support_1", "IFI_Support_2"), ",")

# Cleaning up complaint sector data
unique(complaints$Sector)
complaints$Sector <- gsub("Extractives \\(oil, gas, mining\\)", "Extractives", complaints$Sector)
  # A few comma-separated values. Can also code for presence of multiples. Maximum of 3
complaints <- complaints %>%
  separate(Sector, c("Sector_1", "Sector_2", "Sector_3"), ",")

# Cleaning up complaint issue data
unique(complaints$Issues)
max(nchar(unique(complaints$Issues))) # Some of these strings are long
  # Printing a list of unique issues
strsplit(complaints$Issues, ", ") %>% 
  melt() %>% 
  select(c(value)) %>% 
  mutate_if(is.factor, as.character) %>%
  unique()
  # Cleaning up qualifiers
complaints$Issues <- gsub("Violence against the community \\(by gov't and/or company\\)", "Violence against the community", complaints$Issues)
complaints$Issues <- gsub("Other retaliation \\(actual or feared\\)", "Other retaliation", complaints$Issues)
complaints$Issues <- gsub("Displacement \\(physical and/or economic\\)", "Displacement", complaints$Issues)
  # Figuring out how many columns to split issues into
max(str_count(complaints$Issues, pattern = ",")) # 9
complaints <- complaints %>%
  separate(Issues, c("Issues_1", "Issues_2", "Issues_3", "Issues_4", "Issues_5", "Issues_6", "Issues_7", "Issues_8", "Issues_9", "Issues_10"), ",")

# Cleaning up non eligibility reasons
unique(complaints$If_No_Eligibility_Why)
max(nchar(unique(complaints$If_No_Eligibility_Why)), na.rm = TRUE) # Some of these strings are long
  # Printing a list of unique issues
complaints$If_No_Eligibility_Why <- gsub("\\s*,\\s*", ",", complaints$If_No_Eligibility_Why)
complaints$If_No_Eligibility_Why <- stringr::str_trim(complaints$If_No_Eligibility_Why, side = "both")
strsplit(complaints$If_No_Eligibility_Why, ",") %>% 
  melt() %>% 
  select(c(value)) %>% 
  mutate_if(is.factor, as.character) %>%
  unique()
  
  # Deduping comma separated list before splitting into columns
tmp <- complaints %>% select(c(Complaint_Name, External_ID, If_No_Eligibility_Why)) %>% data.frame()
tmp_copy <- tmp

for(i in 1:nrow(tmp)){
  count <- str_count(tmp$If_No_Eligibility_Why[i], pattern = ",") 
  d <- unlist(strsplit(tmp[i,3], split=","))
  tmp[i,3] <- ifelse(count > 0, paste(d[-which(duplicated(d))], collapse = ","), tmp[i,3])
}

col_order <- names(complaints)
complaints$If_No_Eligibility_Why <- NULL
complaints <- merge(complaints, tmp, by = c("Complaint_Name", "External_ID"))
complaints <- complaints %>% select(col_order)
complaints$If_No_Eligibility_Why[which(complaints$If_No_Eligibility_Why == "")] <- NA

  # Figuring out how many columns to split issues into
max(str_count(complaints$If_No_Eligibility_Why, pattern = ","), na.rm = TRUE) # 3
complaints <- complaints %>%
  separate(If_No_Eligibility_Why, c("If_No_Eligibility_Why_1", "If_No_Eligibility_Why_2", "If_No_Eligibility_Why_3"), ",")
# complaints$If_No_Eligibility_Why_1[which(complaints$If_No_Eligibility_Why_1 == "Unknown")] <- NA
# complaints$If_No_Eligibility_Why_2[which(complaints$If_No_Eligibility_Why_2 == "Unknown")] <- NA
# complaints$If_No_Eligibility_Why_3[which(complaints$If_No_Eligibility_Why_3 == "Unknown")] <- NA

# Dispute_Resolution_Start
sum(is.na(complaints$Dispute_Resolution_Start)) # Counting vals for writeup

# Dispute_Resolution_End
sum(is.na(complaints$Dispute_Resolution_End)) # Counting vals for writeup

# Dispute_Resolution_Status
unique(complaints$Dispute_Resolution_Status)
sum(is.na(complaints$Dispute_Resolution_Status))

# If_No_Dispute_Resolution_Why
unique(complaints$If_No_Dispute_Resolution_Why)
# complaints$If_No_Dispute_Resolution_Why[which(complaints$If_No_Dispute_Resolution_Why == "Unknown")] <- NA
sum(is.na(complaints$If_No_Dispute_Resolution_Why))

# Compliance_Review_Start
sum(is.na(complaints$Compliance_Review_Start)) # Counting vals for writeup
# Compliance_Review_End
sum(is.na(complaints$Compliance_Review_End)) # Counting vals for writeup
# Compliance_Review_Status
unique(complaints$Compliance_Review_Status)
sum(is.na(complaints$Compliance_Review_Status))

# Cleaning up reasons for no compliance report (these are pretty good)
unique(complaints$If_No_Compliance_Report_Why)
  # Not necessary to comma separate (also, some of the reasons themselves contain commas)
# complaints$If_No_Compliance_Report_Why[which(complaints$If_No_Compliance_Report_Why == "Unknown")] <- NA
sum(is.na(complaints$If_No_Compliance_Report_Why))

# Monitoring_Start
sum(is.na(complaints$Monitoring_Start)) # Counting vals for writeup
# Monitoring_End
sum(is.na(complaints$Monitoring_End)) # Counting vals for writeup
# Monitoring_Status
unique(complaints$Monitoring_Status)
sum(is.na(complaints$Monitoring_Status))

# Cleaning up reasons for not monitoring (also pretty good)
unique(complaints$If_No_Monitoring_Why)
  # Not necessary to comma separate 
complaints$If_No_Monitoring_Why[which(complaints$If_No_Monitoring_Why %in% c("N/A"))] <- NA

# Logic to determine final eligibility of complaint
sum(complaints$Eligibility_Status == "closed_with_outcome" & complaints$Status != "Active", na.rm = TRUE)

complaints$ELIGIBLE <- ifelse(complaints$Status != "Active" & complaints$Eligibility_Status == "closed_with_outcome", 1, 0)
complaints$ELIGIBLE[which(complaints$Status == "Active")] <- NA

# Saving data
write.csv(complaints, file = "accountability_console_data_cleaned.csv", na = "", row.names = FALSE)
save(complaints, file = "accountability_console_data_cleaned.RData")

## Fixing up Benchmarks data now

# Fixing up one question from Samer's list first
benchmarks$AfDB_IRM[which(benchmarks$Benchmark == "Is the CR conducted by the mechanism staff, independent experts/panelists, or both?")] <- "Experts"
benchmarks$ADB_SPF_CRP[which(benchmarks$Benchmark == "Is the CR conducted by the mechanism staff, independent experts/panelists, or both?")] <- "Staff"
benchmarks$EBRD_PCM[which(benchmarks$Benchmark == "Is the CR conducted by the mechanism staff, independent experts/panelists, or both?")] <- "Experts"
benchmarks$EIB_CM[which(benchmarks$Benchmark == "Is the CR conducted by the mechanism staff, independent experts/panelists, or both?")] <- "Both"
benchmarks$IFC_CAO[which(benchmarks$Benchmark == "Is the CR conducted by the mechanism staff, independent experts/panelists, or both?")] <- "Both"
benchmarks$IDB_MICI[which(benchmarks$Benchmark == "Is the CR conducted by the mechanism staff, independent experts/panelists, or both?")] <- "Both"
benchmarks$OPIC_OA[which(benchmarks$Benchmark == "Is the CR conducted by the mechanism staff, independent experts/panelists, or both?")] <- "Both"
benchmarks$WB_Panel[which(benchmarks$Benchmark == "Is the CR conducted by the mechanism staff, independent experts/panelists, or both?")] <- "Both"
  
benchmarks_melted <- melt(benchmarks, id.vars = c("Category", "Benchmark"))
benchmarks_melted$value <- toupper(benchmarks_melted$value)
unique(benchmarks_melted$value)
benchmarks_melted$value[which(benchmarks_melted$value == "YES")] <- 1
benchmarks_melted$value[which(benchmarks_melted$value == "NO")] <- 0
benchmarks_melted$value[which(benchmarks_melted$value == "N/A")] <- NA
benchmarks_melted$value[which(grepl("N/A", benchmarks_melted$value))] <- NA
benchmarks_melted$value[which(benchmarks_melted$value == "")] <- NA
  # I am assuming all values will be in days, so the following cleaning process takes away text fields like
  # "day", "dys" etc and where appropriate converts months to days.
grep("days|day|dy|dys", benchmarks_melted$value, ignore.case = TRUE)
  # benchmarks_melted$value <- ifelse(grepl("days|day|dy|dys", benchmarks_melted$value, ignore.case = TRUE), gsub("\\D", "", benchmarks_melted$value), benchmarks_melted$value)

## Some rapid-fire manual cleanup
# benchmarks_cast <- dcast(data = benchmarks_melted, formula = Category + Benchmark ~ variable) %>% t() %>% data.frame()
# benchmarks_melted_non_numeric <- benchmarks_melted %>% 
#   filter(!(is.na(value)) & !(value %in% c(0, 1))) %>% 
#   filter(grepl("\\D", x = value))

# benchmarks_melted_non_numeric$value[which(benchmarks_melted_non_numeric$value == "10 DAYS")] <- 10
# benchmarks_melted_non_numeric$value[which(benchmarks_melted_non_numeric$value == "120 DAYS.")] <- 120
# benchmarks_melted_non_numeric$value[which(benchmarks_melted_non_numeric$value == "~180 DAYS. THIS EXCLUDES TIME FOR TRANSLATION, REQUESTS FOR EXTENSION TO PROVIDE INFORMATION OR FILE DOCUMENT, AND THE TIME NEEDED FOR THE PARTIES TO FACILITATE THE RESOLUTION OF THEIR PROBLEMS.")] <- 180
# benchmarks_melted_non_numeric$value[which(benchmarks_melted_non_numeric$value == "~200 DAYS, NOT TIME BOUNDED. THIS EXCLUDES TIME FOR TRANSLATION, REQUESTS FOR EXTENSION TO PROVIDE INFORMATION OR FILE DOCUMENT, AND THE TIME FOR CONDUCTING THE COMPLIANCE REVIEW, WHICH IS NOT TIME BOUND.")] <- 200
# benchmarks_melted_non_numeric$value[which(benchmarks_melted_non_numeric$value == "10 DAYS FOR ACKNOWLEDGEMENT. 140 DAYS AFTER ACKNOWLEDGEMENT OF THE RECEIPT IS THE GENERAL DEADLINE FOR THE RESPONSE TO ENVIRONMENTAL AND SOCIAL COMPLAINTS. TIMETABLE OF THE COMPLIANCE REVIEW ESTABLISHED IN THE TOR. DEFINED TIMELINES FOR MEDIATION AGREED TO BY THE PARTIES.")] <- 140
# benchmarks_melted_non_numeric$value[which(benchmarks_melted_non_numeric$value == "12 MTHS, DIRECTOR CAN EXTEND")] <- 365
# benchmarks_melted_non_numeric$value[which(benchmarks_melted_non_numeric$value == "135 DAYS. 15 DAYS FOR ELIGIBILITY SCREENING AND 120 DAYS FOR ASSESSMENT.")] <- 135
# benchmarks_melted_non_numeric$value[which(benchmarks_melted_non_numeric$value == "140 DAYS AFTER ACKNOWLEDGEMENT OF THE RECEIPT IS THE GENERAL DEADLINE FOR THE RESPONSE TO ENVIRONMENTAL AND SOCIAL COMPLAINTS. DEFINED TIMELINES AGREED TO BY THE PARTIES.")] <- 140
# benchmarks_melted_non_numeric$value[which(benchmarks_melted_non_numeric$value == "140 DAYS AFTER ACKNOWLEDGEMENT OF THE RECEIPT IS THE GENERAL DEADLINE FOR THE RESPONSE TO ENVIRONMENTAL AND SOCIAL COMPLAINTS. TIMETABLE OF THE COMPLIANCE REVIEW ESTABLISHED IN THE TOR.")] <- 140
# benchmarks_melted_non_numeric$value[which(benchmarks_melted_non_numeric$value == "15 DAYS (ELIGIBILITY). NO SEPARATE REGISTRATION STEP, BUT ELIGIBILITY DETERMINED WITHIN 15 DAYS.")] <- 15
# benchmarks_melted_non_numeric$value[which(benchmarks_melted_non_numeric$value == "15 DAYS FOR ELIGIBILITY. NO SEPARATE REGISTRATION STEP.")] <- 15
# benchmarks_melted_non_numeric$value[which(benchmarks_melted_non_numeric$value == "15 DAYS. THE USE OF THE PILOT APPROACH MAY AFFECT THIS TIMELINE.")] <- 15
# benchmarks_melted_non_numeric$value[which(benchmarks_melted_non_numeric$value == "14 DAYS")] <- 14
# benchmarks_melted_non_numeric$value[which(benchmarks_melted_non_numeric$value == "2 DAYS")] <- 2
# benchmarks_melted_non_numeric$value[which(benchmarks_melted_non_numeric$value == "20 DAYS FOR ELIGIBILITY (NO SEPARATE REGISTRATION PROCESS, ONLY ELIGIBILITY THEN ASSESSMENT).")] <- 20
# benchmarks_melted_non_numeric$value[which(benchmarks_melted_non_numeric$value == "21 BUSINESS DAYS AFTER MANAGEMENT RESPONSE")] <- 21
# benchmarks_melted_non_numeric$value[which(benchmarks_melted_non_numeric$value == "26 DAYS AFTER REGISTRATION")] <- 26
# benchmarks_melted_non_numeric$value[which(benchmarks_melted_non_numeric$value == "47 DYS AFTER RCPT")] <- 47
# benchmarks_melted_non_numeric$value[which(benchmarks_melted_non_numeric$value == "5 BUSINESS DAYS")] <- 5
# benchmarks_melted_non_numeric$value[which(benchmarks_melted_non_numeric$value == "5 DAYS")] <- 5
# benchmarks_melted_non_numeric$value[which(benchmarks_melted_non_numeric$value == "APPROX. 31 DAYS.")] <- 31
# benchmarks_melted_non_numeric$value[which(benchmarks_melted_non_numeric$value == "APPROX. 33 DAYS.")] <- 33
# benchmarks_melted_non_numeric$value[which(benchmarks_melted_non_numeric$value == "APPROX. 60 DAYS: FOR ENVIRONMENTAL AND SOCIAL IMPACTS, AND GOVERNANCE COMPLAINTS. THE CM PREPARES AN ASSESSMENT REPORT WITHIN 40 DAYS OF ADMISSIBILITY.  5 DAYS FOR COMMENTS FROM EIB OPERATIONAL SERVICES AND COMPLAINANTS (NON-CONSECUTIVE) AND AN ADDITIONAL 10 DAYS FOR DIRECTOR GENERAL RESPONSE = 60 DAYS.")] <- 60
# benchmarks_melted_non_numeric$value[which(benchmarks_melted_non_numeric$value == "AROUND 40 DAYS AFTER SUBMISSION OF BANK MANAGEMENT RESPONSE TO COMPLAINT.\nTHERE ARE NO CLEAR TIMELINES FOR THE PROCESSES DESCRIBED IN PARAS. 32-33.")] <- 40

benchmarks_melted$value[which(benchmarks_melted$value == "10 DAYS")] <- 10
benchmarks_melted$value[which(benchmarks_melted$value == "120 DAYS.")] <- 120
benchmarks_melted$value[which(benchmarks_melted$value == "~180 DAYS. THIS EXCLUDES TIME FOR TRANSLATION, REQUESTS FOR EXTENSION TO PROVIDE INFORMATION OR FILE DOCUMENT, AND THE TIME NEEDED FOR THE PARTIES TO FACILITATE THE RESOLUTION OF THEIR PROBLEMS.")] <- 180
benchmarks_melted$value[which(benchmarks_melted$value == "~200 DAYS, NOT TIME BOUNDED. THIS EXCLUDES TIME FOR TRANSLATION, REQUESTS FOR EXTENSION TO PROVIDE INFORMATION OR FILE DOCUMENT, AND THE TIME FOR CONDUCTING THE COMPLIANCE REVIEW, WHICH IS NOT TIME BOUND.")] <- 200
benchmarks_melted$value[which(benchmarks_melted$value == "10 DAYS FOR ACKNOWLEDGEMENT. 140 DAYS AFTER ACKNOWLEDGEMENT OF THE RECEIPT IS THE GENERAL DEADLINE FOR THE RESPONSE TO ENVIRONMENTAL AND SOCIAL COMPLAINTS. TIMETABLE OF THE COMPLIANCE REVIEW ESTABLISHED IN THE TOR. DEFINED TIMELINES FOR MEDIATION AGREED TO BY THE PARTIES.")] <- 140
benchmarks_melted$value[which(benchmarks_melted$value == "12 MTHS, DIRECTOR CAN EXTEND")] <- 365
benchmarks_melted$value[which(benchmarks_melted$value == "135 DAYS. 15 DAYS FOR ELIGIBILITY SCREENING AND 120 DAYS FOR ASSESSMENT.")] <- 135
benchmarks_melted$value[which(benchmarks_melted$value == "140 DAYS AFTER ACKNOWLEDGEMENT OF THE RECEIPT IS THE GENERAL DEADLINE FOR THE RESPONSE TO ENVIRONMENTAL AND SOCIAL COMPLAINTS. DEFINED TIMELINES AGREED TO BY THE PARTIES.")] <- 140
benchmarks_melted$value[which(benchmarks_melted$value == "140 DAYS AFTER ACKNOWLEDGEMENT OF THE RECEIPT IS THE GENERAL DEADLINE FOR THE RESPONSE TO ENVIRONMENTAL AND SOCIAL COMPLAINTS. TIMETABLE OF THE COMPLIANCE REVIEW ESTABLISHED IN THE TOR.")] <- 140
benchmarks_melted$value[which(benchmarks_melted$value == "15 DAYS (ELIGIBILITY). NO SEPARATE REGISTRATION STEP, BUT ELIGIBILITY DETERMINED WITHIN 15 DAYS.")] <- 15
benchmarks_melted$value[which(benchmarks_melted$value == "15 DAYS FOR ELIGIBILITY. NO SEPARATE REGISTRATION STEP.")] <- 15
benchmarks_melted$value[which(benchmarks_melted$value == "15 DAYS. THE USE OF THE PILOT APPROACH MAY AFFECT THIS TIMELINE.")] <- 15
benchmarks_melted$value[which(benchmarks_melted$value == "14 DAYS")] <- 14
benchmarks_melted$value[which(benchmarks_melted$value == "2 DAYS")] <- 2
benchmarks_melted$value[which(benchmarks_melted$value == "20 DAYS FOR ELIGIBILITY (NO SEPARATE REGISTRATION PROCESS, ONLY ELIGIBILITY THEN ASSESSMENT).")] <- 20
benchmarks_melted$value[which(benchmarks_melted$value == "21 BUSINESS DAYS AFTER MANAGEMENT RESPONSE")] <- 21
benchmarks_melted$value[which(benchmarks_melted$value == "26 DAYS AFTER REGISTRATION")] <- 26
benchmarks_melted$value[which(benchmarks_melted$value == "47 DYS AFTER RCPT")] <- 47
benchmarks_melted$value[which(benchmarks_melted$value == "5 BUSINESS DAYS")] <- 5
benchmarks_melted$value[which(benchmarks_melted$value == "5 DAYS")] <- 5
benchmarks_melted$value[which(benchmarks_melted$value == "APPROX. 31 DAYS.")] <- 31
benchmarks_melted$value[which(benchmarks_melted$value == "APPROX. 33 DAYS.")] <- 33
benchmarks_melted$value[which(benchmarks_melted$value == "APPROX. 60 DAYS: FOR ENVIRONMENTAL AND SOCIAL IMPACTS, AND GOVERNANCE COMPLAINTS. THE CM PREPARES AN ASSESSMENT REPORT WITHIN 40 DAYS OF ADMISSIBILITY.  5 DAYS FOR COMMENTS FROM EIB OPERATIONAL SERVICES AND COMPLAINANTS (NON-CONSECUTIVE) AND AN ADDITIONAL 10 DAYS FOR DIRECTOR GENERAL RESPONSE = 60 DAYS.")] <- 60
benchmarks_melted$value[which(benchmarks_melted$value == "AROUND 40 DAYS AFTER SUBMISSION OF BANK MANAGEMENT RESPONSE TO COMPLAINT.\nTHERE ARE NO CLEAR TIMELINES FOR THE PROCESSES DESCRIBED IN PARAS. 32-33.")] <- 40

highlighted_questions <- c(
"Is the CR conducted by the mechanism staff, independent experts/panelists, or both?",
"Does the mechanism have the independent authority to accept and conduct CR?",
"If CR is sought, must PS occur first?",
"Does the policy contain restrictions concerning past or ongoing judicial, arbitral, or administrative proceedings?",
"Does the policy contain restrictions concerning past or ongoing IAM proceedings?",
"May the mechanism conduct compliance review for completed projects?",
"May the mechanism conduct problem solving for completed projects?",
"May a claim be brought after full disbursal of funds?",
"May a claim be brought after physical completion of the project?",
"May a claim be brought before a project is approved by the institution's Board?",
"May claimants make comments on draft findings?",
"Are draft findings made available to claimant?",
"Must management prepare an action plan in consultation with requestors? "
)

benchmarks_highlighted <- benchmarks %>% filter(Benchmark %in% highlighted_questions)
benchmarks_melted_highlighted <- benchmarks_melted %>% filter(Benchmark %in% highlighted_questions)

## Good enough for me! 

benchmarks_cleaned <- dcast(data = benchmarks_melted, formula = Category + Benchmark ~ variable) %>% data.frame()

# Saving data
write.csv(benchmarks_cleaned, file = "benchmark_data_cleaned.csv", na = "", row.names = FALSE)
write.csv(benchmarks_melted, file = "benchmark_data_cleaned_melted.csv", na = "", row.names = FALSE)
save(benchmarks_cleaned, file = "benchmark_data_cleaned.RData")
save(benchmarks_melted, file = "benchmark_data_cleaned_melted.RData")
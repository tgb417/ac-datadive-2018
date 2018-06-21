from builtins import str
from builtins import range
from builtins import object

import time
import unicodecsv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from accountability_console.models import Complaint, IAM

def scrape():
    with open('cao_scraped.csv', 'wb') as file:
        writer = unicodecsv.writer(file)
        header = [
            'IAM',
            'Year',
            'Country',
            'Project',
            'ID',
            'IAM ID',
            'Filer(s)',
            'Environmental Category',
            'Project Company',
            'Project Number',
            'Related Project Number',
            'Project Type',
            'Financial Institution',
            'Project Loan Amount',
            'Sector',
            'Issues',
            'Complaint Status',
            'Filing Date',
            'Registration Start Date',
            'Registration End Date',
            'Eligibility Start Date',
            'Eligibility End Date',
            'Dispute Resolution Start Date',
            'Dispute Resolution End Date',
            'Compliance Review Start Date',
            'Compliance Review End Date',
            'Monitoring Start Date',
            'Monitoring End Date',
            'Date Closed',
            'Documents',
            'Hyperlink'
        ]
        writer.writerow(header)
        driver = webdriver.Chrome()
        cao_scrape(driver, writer)
        time.sleep(2)
        driver.quit()

def cao_scrape(driver, writer):
    driver.get('http://www.cao-ombudsman.org/cases/default.aspx')
    time.sleep(2)
    button = driver.find_element_by_id('ctl00_MainContent_btnSearch').click()
    time.sleep(2)
    tables = driver.find_elements_by_xpath('//*[@id="ctl00_MainContent_divResults"]/ul')
    table_range = range(1, len(tables)+1)
    for table in table_range:
        rows = driver.find_elements_by_xpath('//*[@id="ctl00_MainContent_divResults"]/ul[%s]/li' % table)
        row_range = range(1, len(rows)+1)
        for row in row_range:
            functions = driver.find_elements_by_xpath('//*[@id="ctl00_MainContent_divResults"]/ul[%s]/li[%s]/ul/li' % (table, row))
            function_range = range(1, len(functions)+1)
            for function in function_range:
                complaints = driver.find_elements_by_xpath('//*[@id="ctl00_MainContent_divResults"]/ul[%s]/li[%s]/ul/li[%s]/ul/li' % (table, row, function))
                complaint_range = range(1, len(complaints)+1)
                for complaint in complaint_range:
                    link = driver.find_element_by_xpath('//*[@id="ctl00_MainContent_divResults"]/ul[%s]/li[%s]/ul/li[%s]/ul/li[%s]/a' % (table, row, function, complaint))
                    link.click()
                    time.sleep(2)
                    project_and_id = driver.find_element_by_id('ctl00_MainContent_ctrlProjectName').text
                    project, project_id = project_and_id.rsplit(' ', 1)
                    country = driver.find_element_by_id('ctl00_MainContent_ctrlProjectCountries').text
                    year = driver.find_element_by_id('ctl00_MainContent_ctrlDateFilled').text
                    year = year[-4:]
                    url = driver.current_url
                    case_id = ''.join([i for i in url if i.isdigit()])
                    environmental_category = driver.find_element_by_id('ctl00_MainContent_ctrlEnvironmentCategory').text
                    project_type = driver.find_element_by_id('ctl00_MainContent_ctrlDepartment').text
                    sector = driver.find_element_by_id('ctl00_MainContent_ctrlSector').text
                    financial_institution = driver.find_element_by_id('ctl00_MainContent_ctrlInstitution').text
                    project_company = driver.find_element_by_id('ctl00_MainContent_ctrlCompany').text
                    project_loan = driver.find_element_by_id('ctl00_MainContent_ctrlCommitment').text
                    issues = driver.find_element_by_id('ctl00_MainContent_ctrlConcerns').text
                    case_status = driver.find_element_by_id('ctl00_MainContent_ctrlCaseStatus').text
                    try: 
                        completed_stage = driver.find_elements_by_class_name('completed')
                        last_completed_stage = completed_stage[-1].text
                    except IndexError: 
                        closed_stage = driver.find_element_by_class_name('closed')
                        last_completed_stage = closed_stage.text
                    try: 
                        active_stage = driver.find_element_by_class_name('inprocess')
                    except NoSuchElementException:
                        active_stage = None
                    if active_stage in ('Eligibility: In Process', 'Eligible: In Process'):
                        eligibility_start_date = 'Completed'
                    else: 
                        eligibility_start_date = None
                    if last_completed_stage in ('Eligibility: Completed', 'Eligible: Completed'):
                        eligibility_end_date = 'Completed'
                    else: 
                        eligibility_end_date = None
                    if active_stage in ('Assessment Period: In Process', 'Facilitating Settlement: Active'):
                        dr_start_date = 'Completed'
                    elif last_completed_stage == 'Assessment Period: Completed':
                        dr_start_date = 'Completed'
                    else: 
                        dr_start_date = None 
                    if last_completed_stage == 'Facilitating Settlement: Completed':
                        dr_end_date = 'Completed'
                    else: 
                        dr_end_date = None
                    if active_stage in ('Monitoring/Close Out: In Process', 'Monitoring: In Process'):
                        monitoring_start_date = 'Completed'
                    else: 
                        monitoring_start_date = None    
                    if last_completed_stage == 'Monitoring/Close Out: Completed':
                        monitoring_end_date = 'Completed'
                    else: 
                        monitoring_end_date = None
                    if active_stage in ('Under Appraisal: In Process', 'Under Audit: In Process'):
                        cr_start_date = 'Completed'
                    elif last_completed_stage == 'Under Appraisal: Completed':
                        cr_start_date = 'Completed'
                    else: 
                        cr_start_date = None
                    if last_completed_stage == 'Under Audit: Compelted':
                        cr_end_date = 'Completed'
                    else: 
                        cr_end_date = None
                    if last_completed_stage == 'Monitoring: Completed':
                        date_closed = 'Completed'
                    else: 
                        date_closed = None
                    date_filed = driver.find_element_by_id('ctl00_MainContent_ctrlDateFilled').text
                    registration_start_date = date_filed
                    registration_end_date = None
                    row_data = [
                        'CAO',
                        year,
                        country,
                        project,
                        case_id,
                        21,
                        None,
                        environmental_category,
                        project_company,
                        project_id,
                        None,
                        project_type,
                        financial_institution,
                        project_loan,
                        sector,
                        issues,
                        case_status,
                        date_filed,
                        registration_start_date,
                        registration_end_date,
                        eligibility_start_date,
                        eligibility_end_date,
                        dr_start_date,
                        dr_end_date,
                        cr_start_date,
                        cr_end_date,
                        None,
                        monitoring_end_date,
                        date_closed,
                        None,
                        driver.current_url,
                    ]
                    writer.writerow(row_data)
                    print(row_data)
                    driver.execute_script('window.history.go(-1)')
                    time.sleep(0.7)
    return True

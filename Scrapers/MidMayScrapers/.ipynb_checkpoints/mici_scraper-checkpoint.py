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
    with open('mici_scraped.csv', 'wb') as file:
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
            'Hyperlink',
        ]
        writer.writerow(header)
        driver = webdriver.Chrome()
        mici_scrape(driver, writer)
        time.sleep(2)
        driver.quit()

def mici_scrape(driver, writer):
    driver.get("https://idblegacy.iadb.org/en/mici/by-country,7631.html")
    time.sleep(2)
    page_range = range(2,14)
    rows = driver.find_elements_by_xpath('//*[@id="searchResults"]/li')
    for page in page_range:
        row_range = range(1, len(rows)+1)
        for row in row_range:
            project_and_id = driver.find_element_by_xpath('//*[@id="searchResults"]/li[%s]/h5/a' % row).text
            try:
                project, case_id = project_and_id.rsplit(' (', 1)
            except:
                project = None
                case_id = project_and_id
            case_id = case_id.replace(')','')
            country_and_year = driver.find_element_by_xpath('//*[@id="searchResults"]/li[%s]/div/span[1]' % row).text
            country, year = country_and_year.split(' - ')
            project_link = driver.find_element_by_xpath('//*[@id="searchResults"]/li[%s]/h5/a' % row)
            project_link.click()
            time.sleep(2)
            complaint_status_string = driver.find_element_by_xpath('//*[@id="container_2"]/div/div/div/div[2]/table/tbody/tr[2]/td[1]/p').text 
            junk, complaint_status = complaint_status_string.rsplit(':  ', 1)
            try: 
                filers = driver.find_element_by_xpath('//*[@id="container_2"]/div/div/div/div[2]/table/tbody/tr[3]/td/div[2]/div/p[2]').text
            except NoSuchElementException:
                filers = None
            try:
                for i in range(1, 8):
                    header = driver.find_element_by_xpath('//*[@id="container_2"]/div/div/div/div[3]/div/b[%s]' % i)
                    if header.text == 'Project Number:':
                        project_number_xpath = '//*[@id="container_2"]/div/div/div/div[3]/div/p[%s]' % i
                        project_number = driver.find_element_by_xpath(project_number_xpath).text
                    elif header.text == 'Other related projects:':
                        related_project_xpath = '//*[@id="container_2"]/div/div/div/div[3]/div/p[%s]' % i
                        related_project_number = driver.find_element_by_xpath(related_project_xpath).text
                    elif header.text == 'Environmental Category:':
                        environmental_category_xpath = '//*[@id="container_2"]/div/div/div/div[3]/div/p[%s]' % i
                        environmental_category = driver.find_element_by_xpath(environmental_category_xpath).text
                    elif header.text == 'Project Name:':
                        project_name_xpath = '//*[@id="container_2"]/div/div/div/div[3]/div/p[%s]' % i
                        project_name = driver.find_element_by_xpath(project_name_xpath).text
                    elif header.text == 'Sector:':
                        sector_xpath = '//*[@id="container_2"]/div/div/div/div[3]/div/p[%s]' % i
                        sector = driver.find_element_by_xpath(sector_xpath).text
                    elif header.text == 'Project Type:':
                        project_type_xpath = '//*[@id="container_2"]/div/div/div/div[3]/div/p[%s]' % i
                        project_type = driver.find_element_by_xpath(project_type_xpath).text
                    elif header.text == 'IDB Financing:':
                        idb_financing_xpath = '//*[@id="container_2"]/div/div/div/div[3]/div/p[%s]' % i
                        financing = driver.find_element_by_xpath(idb_financing_xpath).text
            except NoSuchElementException: 
                related_project = None
            if year > '2014':
                try:
                    completed_reg = driver.find_elements_by_class_name('sltgray')
                    last_completed_reg = completed_reg[-1].text.strip()
                    print(last_completed_reg)
                except IndexError:
                    last_completed_reg = None
                    print('No Registration Undertaken')
                if last_completed_reg in ('Registration Not registered'):
                    registration_start_date = 'Completed'
                    registration_end_date = None
                else: 
                    registration_start_date = None
                    registration_end_date = None
                if last_completed_reg in ('Eligibility Eligible', 'Eligibility', 'Eligibility Not eligible'):
                    eligibility_start_date = 'Completed'
                    eligibility_end_date = 'Completed'
                else:
                    eligibility_start_date = None
                    eligibility_end_date = None
                try:
                    completed_dr = driver.find_elements_by_class_name('sltgreen')
                    last_completed_dr = completed_dr[-1].text.strip()
                    print(last_completed_dr)
                except IndexError:
                    last_completed_dr = None
                    print('No Dispute Resolution Undertaken')
                if last_completed_dr in ('Assessment', 'Assessment Transferred'):
                    dr_start_date = 'Completed'
                else: 
                    dr_start_date = None
                if last_completed_dr == 'Consultation Process':
                    dr_end_date = 'Completed'
                else: 
                    dr_end_date = None
                if last_completed_dr == 'Monitoring':
                    if complaint_status == 'Open':
                        monitoring_start_date = 'Completed'
                    elif complaint_status == 'Closd':
                        monitoring_end_date = 'Completed'
                        date_closed = 'Completed'
                else: 
                    monitoring_start_date = None
                    monitoring_end_date = None
                    date_closed = None
                try: 
                    completed_cr = driver.find_elements_by_class_name('cuadro_dw_azul')
                    last_completed_cr = completed_cr[-1].text.strip()
                    print(last_completed_cr)
                except IndexError:
                    last_completed_cr = None
                    print('No Compliance Review Undertaken')
                if last_completed_cr == 'Monitoring':
                    if complaint_status == 'Open':
                        monitoring_start_date = 'Completed'
                    elif complaint_status == 'Closed':
                        monitoring_end_date = 'Completed'
                        date_closed = 'Completed'
                else: 
                    monitoring_start_date = None
                    monitoring_end_date = None  
                    date_closed = None
                if last_completed_cr in ('Recommendation for a CR and ToRs', 'Investigation'):
                    cr_start_date = 'Completed'
                else: 
                    cr_start_date = None
                if last_completed_cr in ('CR Report', 'Recommendation for a CR and ToRs Closed', 'Investigation Closed'):
                    cr_end_date = 'Completed'
                else: 
                    cr_end_date = None
            elif year <= '2014':
                stages = driver.find_elements_by_xpath('//*[@id="container_2"]/div/div/div/div[4]/div/div[1]/div')
                stage_range = range(1, len(stages)+1)
                for stage in stage_range:
                    try: 
                        completed_dr = driver.find_elements_by_class_name('cuadro_dw')
                        last_completed_dr = completed_dr[-1].text.strip()
                    except IndexError:
                        last_completed_dr = None
                    try: 
                        completed_cr = driver.find_elements_by_class_name('cuadro_dw_naranja')
                        last_completed_cr = completed_cr[-1].text.strip()
                    except IndexError:
                        last_completed_cr = None
                    if last_completed_dr == 'Eligibility':
                        eligibility_end_date = 'Completed'
                    elif last_completed_cr == 'Eligibility':
                        eligibility_end_date = 'Completed'
                    else:
                        eligibility_end_date = None
                    if last_completed_dr == 'Assessment':
                        dr_start_date = 'Completed'
                    else:
                        dr_start_date = None
                    if last_completed_dr == 'Consultation Phase Exercise':
                        dr_end_date = 'Completed'
                    else:
                        dr_end_date = None
                    if last_completed_dr == 'Monitoring':
                        monitoring_end_date = 'Completed'
                    elif last_completed_cr == 'Monitoring':
                        monitoring_end_date = 'Completed'
                    else:
                        monitoring_end_date = None
                    if last_completed_cr in ('Preparation of TORs', 'Investigation'):
                        cr_start_date = 'Completed'
                    else:
                        cr_start_date = None
                    if last_completed_cr == 'Panel Report':
                        cr_end_date = 'Completed'
                    else:
                        cr_end_date = None
            row_data = [
                'MICI',
                year,
                country,
                project_name,
                case_id,
                24,
                filers,
                environmental_category,
                None,
                project_number,
                related_project_number,
                project_type,
                None,
                financing,
                sector,
                None,
                complaint_status,
                None,
                registration_start_date,
                registration_end_date,
                eligibility_start_date,
                eligibility_end_date,
                dr_start_date,
                dr_end_date,
                cr_start_date,
                cr_end_date,
                monitoring_start_date,
                monitoring_end_date,
                date_closed,
                None,
                driver.current_url,
            ]
            writer.writerow(row_data)
            print(row_data)
            time.sleep(0.25)
            driver.execute_script('window.history.go(-1)')
            time.sleep(0.7)
        driver.get('https://idblegacy.iadb.org/en/mici/by-country,7631.html?status=&country=url.country&yearDate=&page=%s' % page)
        time.sleep(2)
    return True
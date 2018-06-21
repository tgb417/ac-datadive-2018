from builtins import str
from builtins import range
from builtins import object

import time
import unicodecsv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

def scrape():
    with open('adb_crp_scraped.csv', 'wb') as file:
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
            'Compliance Report Issued?',
            'Date Closed',
            'Documents',
            'Hyperlink',
            'Project Date',
            'Project Status',
            'Project Description',
        ]
        writer.writerow(header)
        driver = webdriver.Chrome()
        adb_crp_scrape(driver, writer)
        time.sleep(2)
        driver.quit()
def adb_crp_scrape(driver, writer):
    driver.get("http://compliance.adb.org/dir0035p.nsf/alldocs/BDAO-7XGAWN?OpenDocument&expandable=2")
    time.sleep(2)
    rows = driver.find_elements_by_xpath('//*[@id="middle"]/table[1]/tbody/tr')
    row_range = range(2, len(rows)+1)
    for row in row_range:
        bad_row = driver.find_element_by_xpath('//*[@id="middle"]/table[1]/tbody/tr[%s]' %row).text
        if bad_row not in (' ', None, ''):
            complaint_number = driver.find_element_by_xpath('//*[@id="middle"]/table[1]/tbody/tr[%s]/td[1]' % row).text
            year, junk = complaint_number.rsplit('/')
            date_filed = driver.find_element_by_xpath('//*[@id="middle"]/table[1]/tbody/tr[%s]/td[2]' % row).text
            project_name = driver.find_element_by_xpath('//*[@id="middle"]/table[1]/tbody/tr[%s]/td[3]/a' % row)
            project_name.click()
            time.sleep(1)
            actual_project_name = driver.find_element_by_xpath('//*[@id="middle"]/table[1]/tbody/tr[3]/td[2]').text
            project_number = driver.find_element_by_xpath('//*[@id="middle"]/table[1]/tbody/tr[4]/td[2]').text
            if project_number in 'Project Number':
                junk, actual_project_number = project_number.split('Project Number ')
            else:
                actual_project_number = project_number
            country = driver.find_element_by_xpath('//*[@id="middle"]/table[1]/tbody/tr[5]/td[2]').text
        row_data = [
            'ADB CRP',
            year,
            country,
            actual_project_name,
            complaint_number,
            25,
            None,
            None,
            None,
            actual_project_number,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            date_filed,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        ]
        if bad_row not in ('', ' ', None):
            writer.writerow(row_data)
            print(row_data)
            time.sleep(0.25)
            driver.execute_script('window.history.go(-1)')
            time.sleep(0.7)
    return True


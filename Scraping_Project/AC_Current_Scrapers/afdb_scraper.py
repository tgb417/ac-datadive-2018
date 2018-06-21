from builtins import str
from builtins import range
from builtins import object

import time
import unicodecsv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

def scrape():
    with open('afdb_scraped.csv', 'wb') as file:
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
        afdb_scrape(driver, writer)
        time.sleep(2)
        driver.quit()

def afdb_scrape(driver, writer):
    driver.get("https://www.afdb.org/en/independent-review-mechanism/management-of-complaints/registered-requests/")
    time.sleep(2)
    rows = driver.find_elements_by_xpath('//*[@id="c136818"]/table/tbody/tr')
    row_range = range(1, len(rows)+1)
    for row in row_range:
        c_link = driver.find_element_by_xpath('//*[@id="c136818"]/table/tbody/tr[%s]/td[1]/a' % row)
        complaint_id = c_link.text
        country_and_project = driver.find_element_by_xpath('//*[@id="c136818"]/table/tbody/tr[%s]/td[2]/a' % row).text
        complaint_id_digits = ''.join([i for i in complaint_id if i.isdigit()])
        year = complaint_id_digits[:4]
        country, project = country_and_project.split(': ', 1)
        # c_link.click()
        # time.sleep(1)
        # div_for_ul_i_want = driver.find_element_by_class_name('primary')
        # list_items = div_for_ul_i_want.find_elements_by_tag_name('li')
        # list_of_link_text_on_complaints = []
        # for i in list_items:
        #     if i not in (list_of_link_text_on_complaints, ''):
        #         list_of_link_text_on_complaints.append(i.text)
        #         registration = 'Notice of registration', 'Notice of Registration'
        row_data = [
            'IRM',
            year,
            country,
            project,
            complaint_id,
            28,
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
            # list_of_link_text_on_complaints,
        ]
        writer.writerow(row_data)
        print(row_data)
        time.sleep(0.5)
        # driver.execute_script('window.history.go(-1)')
        # time.sleep(1)
    return True
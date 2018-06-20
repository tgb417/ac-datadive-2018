from builtins import str
from builtins import range
from builtins import object

import time
import datetime
from datetime import date
import unicodecsv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from accountability_console.models import Complaint, IAM

def scrape():
    with open('eib_projects_scraped.csv', 'wb') as file:
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
            'Project Date',
            'Project Status',
            'Project Status Date (status updated as of month/day/year)'
            'Project Description'
        ]
        writer.writerow(header)
        driver = webdriver.Chrome()
        eib_project_scrape(driver, writer)
        time.sleep(2)
        driver.quit()

def eib_project_scrape(driver, writer):
    driver.get('http://www.eib.org/projects/pipelines/index.htm')
    time.sleep(2)
    select_all = driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[3]/div[1]/select/option[5]')
    select_all.click()
    time.sleep(2)
    button = driver.find_element_by_xpath('//*[@id="footer"]/div[3]/div[2]/div/p/button').click()
    time.sleep(1)
    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
    time.sleep(1)
    rows = driver.find_elements_by_xpath('//*[@id="content"]/div[2]/table/tbody/tr')
    row_range = range(1, len(rows)+1)
    for row in row_range:
        project = driver.find_element_by_xpath('//*[@id="content"]/div[2]/table/tbody/tr[%s]/td[2]/a/span' % row).click()
        time.sleep(2)
        try:
            button = driver.find_element_by_xpath('//*[@id="footer"]/div[3]/div[2]/div/p/button').click()
            time.sleep(1)
        except Exception as error:
            print('No Button, Carry on!')
        project_name = driver.find_element_by_class_name('custom-h2').text
        project_number_text = driver.find_element_by_xpath('//*[@id="details"]/li[1]').text
        junk, project_number = project_number_text.split('Reference: ')
        project_date_text = driver.find_element_by_xpath('//*[@id="details"]/li[2]').text
        junk, project_date = project_date_text.split('Release date: ', 1)
        pday, pmonth, pyear = project_date.split('/')
        new_project_date = '%s/%s/%s' %(pmonth, pday, pyear)
        project_company = driver.find_element_by_xpath('//*[@id="pipeline-content"]/div/div[2]/p').text
        country = driver.find_element_by_xpath('//*[@id="pipeline-content"]/div/ul[2]/li/a').text
        project_description = driver.find_element_by_xpath('//*[@id="pipeline-content"]/div/div[5]').text
        sector_text = driver.find_element_by_xpath('//*[@id="pipeline-content"]/div/ul[3]/li').text
        junk, sector = sector_text.split('\n', 1)
        try: 
            elmguarantee = driver.find_element_by_xpath('//*[@id="pipeline-content"]/div/div[11]')
            if elmguarantee.text == 'elmGuarantee':
                print('elmGuarantee exists')
                loan_amount = driver.find_element_by_xpath('//*[@id="pipeline-content"]/div/p[2]').text
                status_text = driver.find_element_by_xpath('//*[@id="pipeline-content"]/div/p[4]').text
                print(status_text)
            elif elmguarantee.text != 'elmGuarantee':
                print('trying this... ')
                loan_amount = driver.find_element_by_xpath('//*[@id="pipeline-content"]/div/p[1]').text
                status_text = driver.find_element_by_xpath('//*[@id="pipeline-content"]/div/p[3]').text
                print(status_text)
        except Exception as NoSuchElementException:
            print('no elmGuarantee')
            loan_amount = driver.find_element_by_xpath('//*[@id="pipeline-content"]/div/p[1]').text
            status_text = driver.find_element_by_xpath('//*[@id="pipeline-content"]/div/p[3]').text
            print(status_text)
        status, status_date = status_text.split(' - ', 1)
        day, month, year = status_date.split('/')
        new_status_date = '%s/%s/%s' %(month, day, year)
        row_data = [
            'EIB',
            None,
            country,
            project_name,
            None,
            None,
            None,
            None,
            project_company,
            project_number,
            None,
            None,
            None,
            loan_amount,
            sector,
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
            new_project_date,
            status,
            new_status_date,
            project_description,
        ]
        writer.writerow(row_data)
        print(row_data)
        driver.execute_script('window.history.go(-1)')
        time.sleep(0.7)
        select_all = driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[3]/div[1]/select/option[5]')
        select_all.click()
        time.sleep(2)
        driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
        time.sleep(1)
        scroll_modifier = int(row) * 40
        driver.execute_script("window.scrollTo(0, %s)" % scroll_modifier) 
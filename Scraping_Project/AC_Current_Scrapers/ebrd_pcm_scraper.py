from builtins import str
from builtins import range
from builtins import object
from datetime import datetime

import time
import datetime
import unicodecsv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

def scrape():
    with open('ebrd_pcm_scraped.csv', 'wb') as file:
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
        ebrd_pcm_scrape(driver, writer)
        time.sleep(2)
        driver.quit()

def ebrd_pcm_scrape(driver, writer):
    driver.get('http://www.ebrd.com/work-with-us/project-finance/project-complaint-mechanism/pcm-register.html')
    time.sleep(2)
    rows = driver.find_elements_by_xpath('/html/body/div[4]/div[1]/div/div[1]/article/table/tbody/tr')
    row_range = range(4, len(rows)+1)
    for row in row_range:
        complaint_id = driver.find_element_by_xpath('/html/body/div[4]/div[1]/div/div[1]/article/table/tbody/tr[%s]/td[1]' %row).text
        if complaint_id in ('2018', '2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010', ' '):
            print('this is a year: %s' %complaint_id)
        else:
            complaint_id = driver.find_element_by_xpath('/html/body/div[4]/div[1]/div/div[1]/article/table/tbody/tr[%s]/td[1]' %row).text
            print(complaint_id)
            year, junk = complaint_id.split('/')
            registration_start_date = driver.find_element_by_xpath('/html/body/div[4]/div[1]/div/div[1]/article/table/tbody/tr[%s]/td[2]' %row).text
            try:
                project_link = driver.find_element_by_xpath('/html/body/div[4]/div[1]/div/div[1]/article/table/tbody/tr[%s]/td[3]/a' %row)
                if project_link.text == 'PSD':
                    project_link.click()
                    project = driver.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/h1').text
                    country = driver.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/div[1]/p[1]').text
                    project_number = driver.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/div[1]/p[2]').text
                    sector = driver.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/div[1]/p[3]').text
                    environmental_category = driver.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/div[1]/p[5]').text
                    project_date = driver.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/div[1]/p[6]').text
                    project_status = driver.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/div[1]/p[7]').text
                    url = driver.current_url
                elif project_link.text != 'PSD': 
                    try:
                        project_link.click()
                        project = driver.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/h1').text
                        country = driver.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/div[1]/p[1]').text
                        project_number = driver.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/div[1]/p[2]').text
                        sector = driver.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/div[1]/p[3]').text
                        environmental_category = driver.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/div[1]/p[5]').text
                        project_date = driver.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/div[1]/p[6]').text
                        project_status = driver.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/div[1]/p[7]').text
                    except NoSuchElementException:
                        url = driver.current_url
                        print('not here, check this: %s' %url)
            except NoSuchElementException:
                try: 
                    project_link = driver.find_element_by_xpath('/html/body/div[4]/div[1]/div/div[1]/article/table/tbody/tr[%s]/td[3]/p[1]/a' %row)
                    project_link.click()
                    project = driver.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/h1').text
                    country = driver.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/div[1]/p[1]').text                    
                    project_number = driver.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/div[1]/p[2]').text
                    sector = driver.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/div[1]/p[3]').text
                    environmental_category = driver.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/div[1]/p[5]').text                    
                    project_date = driver.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/div[1]/p[6]').text
                    project_status = driver.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/div[1]/p[7]').text
                    url = driver.current_url
                except NoSuchElementException:
                    project_link_td = driver.find_element_by_xpath('/html/body/div[4]/div[1]/div/div[1]/article/table/tbody/tr[%s]/td[3]' %row)
                    project_link = project_link_td.find_elements_by_tag_name('a')
                    for i in project_link:
                        i.click()
                        time.sleep(1)
                        project = driver.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/h1').text
                        country = driver.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/div[1]/p[1]').text
                        project_number = driver.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/div[1]/p[2]').text
                        sector = driver.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/div[1]/p[3]').text
                        environmental_category = driver.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/div[1]/p[5]').text
                        project_date = driver.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/div[1]/p[6]').text
                        project_status = driver.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/div[1]/p[7]').text
                        url = driver.current_url
                        driver.execute_script('window.history.go(-1)')
            row_data = [
                'EBRD PCM',
                year,
                country,
                project,
                complaint_id,
                26,
                None,
                environmental_category,
                None,
                project_number,
                None,
                None,
                None,
                None,
                sector,
                None,
                None,
                None,
                registration_start_date,
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
                url,
                project_date,
                project_status,
                None,
            ]
            writer.writerow(row_data)
            print(row_data)
            driver.execute_script('window.history.go(-1)')
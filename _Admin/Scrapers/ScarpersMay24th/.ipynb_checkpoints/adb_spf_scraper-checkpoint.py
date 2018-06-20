from builtins import str
from builtins import range
from builtins import object

import time
import unicodecsv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

def scrape():
    with open('adb_spf_scraped.csv', 'wb') as file:
        writer = unicodecsv.writer(file)
        header = [
            'IAM',
            'Project Name',
            'Project Number',
            'Country',
            'Project Status',
            'Project Financing',
            'Sector',
        ]
        writer.writerow(header)
        driver = webdriver.Chrome()
        adb_spf_scrape(driver, writer)
        time.sleep(2)
        driver.quit()

def adb_spf_scrape(driver, writer):
    driver.get("https://www.adb.org/site/accountability-mechanism/problem-solving-function/complaint-registry-year")
    time.sleep(2)
    tables = driver.find_elements_by_class_name('table-striped')
    table_range = range(1, len(tables)+1)
    for table in table_range:
        rows = driver.find_elements_by_xpath('/html/body/div/div/div/div/main/table[%s]/tbody/tr' % table)
        row_range = range(1, len(rows)+1)
        print(row_range)
        for row in row_range:
            try:
                project_link = driver.find_element_by_xpath('/html/body/div/div/div/div/main/table[%s]/tbody/tr[%s]/td[2]/a' % (table, row))
                time.sleep(2)
                project_id = driver.find_element_by_xpath('/html/body/div/div/div/div/main/table[%s]/tbody/tr[%s]/td[1]' % (table, row))
            except NoSuchElementException:
                project_link = driver.find_element_by_xpath('/html/body/div/div/div/div/main/table[%s]/tbody/tr[%s]/td[2]' % (table, row))
                time.sleep(2)
            try:
                project_link.click()
                time.sleep(1)
            except NoSuchElementException:
                project_name = project_link
                issues = driver.find_element_by_xpath('/html/body/div/div/div/div/main/table[%s]/tbody/tr[%s]/td[3]/ul/li' % (table, row)).text
                project_id = driver.find_element_by_xpath('/html/body/div/div/div/div/main/table[%s]/tbody/tr[%s]/td[1]' % (table, row)).text
            try:
                project_data = driver.find_element_by_xpath('//*[@id="tabs-0"]/li[2]/a')
                project_data.click()
                time.sleep(1)
                project_rows = driver.find_elements_by_xpath('//*[@id="project-pds"]/div/div/div/table[1]/tbody/tr')
                project_row_range = range(1, len(project_rows))
                for project_row in project_row_range:
                    table_div = driver.find_element_by_xpath('//*[@id="project-pds"]/div/div/div/table[1]/tbody/tr[%s]/td[1]' % project_row)
                    if table_div.text == 'Project Name':
                        project_name = driver.find_element_by_xpath('//*[@id="project-pds"]/div/div/div/table[1]/tbody/tr[%s]/td[2]' % project_row).text
                    elif table_div.text == 'Project Number':
                        project_number = driver.find_element_by_xpath('//*[@id="project-pds"]/div/div/div/table[1]/tbody/tr[%s]/td[2]' % project_row).text
                    elif table_div.text == 'Country':
                        country = driver.find_element_by_xpath('//*[@id="project-pds"]/div/div/div/table[1]/tbody/tr[%s]/td[2]' % project_row).text
                    elif table_div.text == 'Project Status':
                        project_status = driver.find_element_by_xpath('//*[@id="project-pds"]/div/div/div/table[1]/tbody/tr[%s]/td[2]' % project_row).text
                    elif table_div.text == 'Project Type / Modality of Assistance':
                        project_finance_type = driver.find_element_by_xpath('//*[@id="project-pds"]/div/div/div/table[1]/tbody/tr[%s]/td[2]' % project_row).text
                    elif table_div.text == 'Sector / Subsector':
                        sector = driver.find_element_by_xpath('//*[@id="project-pds"]/div/div/div/table[1]/tbody/tr[%s]/td[2]/p/strong' % project_row).text
                    elif table_div.text == 'Description':
                        project_description = driver.find_element_by_xpath('//*[@id="project-pds"]/div/div/div/table[1]/tbody/tr[%s]/td[2]' % project_row).text
                    elif table_div.text == 'Source of Funding / Amount':
                        funds = driver.find_elements_by_class_name('colspan')
                        if funds.count(1):
                            fund_name = funds.text
                            fund_amount = driver.find_element_by_class_name('data-th').text
                        elif funds.count(2):
                            for fund in funds:
                                fund_name = fund.text
                        else: 
                            print('No class')
                                # fund_amount = driver.find
            except NoSuchElementException:
                print ('No Project Link')
            row_data = [
                'ADB SPF',
                project_name,
                project_number,
                country,
                project_status,
                project_finance_type,
                sector,
            ]
            writer.writerow(row_data)
            print(row_data)
            time.sleep(0.25)
            driver.execute_script('window.history.go(-2)')
            time.sleep(0.7)
    return True
    
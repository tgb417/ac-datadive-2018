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
    with open('panel_scraped_new.csv', 'wb') as file:
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
            'Compliance Report Issued?'
        ]
        writer.writerow(header)
        driver = webdriver.Chrome()
        inspection_panel_scrape(driver, writer)
        time.sleep(2)
        driver.quit()

def inspection_panel_scrape(driver, writer):
    driver.get("http://ewebapps.worldbank.org/apps/ip/Pages/AllPanelCases.aspx")
    time.sleep(3)
    rows = driver.find_elements_by_xpath('//*[@id="tblnewAdd"]/tbody/tr')
    row_range = range(2, len(rows)+1)
    for row in row_range:
        iframe = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
        browser.switch_to.frame(iframe)[0]
        case_id = driver.find_element_by_xpath('//*[@id="tblnewAdd"]/tbody/tr[%s]/td[1]' % row).text
        time.sleep(1)
        country = driver.find_element_by_xpath('//*[@id="tblnewAdd"]/tbody/tr[%s]/td[2]' % row).text
        year = driver.find_element_by_xpath('//*[@id="tblnewAdd"]/tbody/tr[%s]/td[3]' % row).text
        project = driver.find_element_by_xpath('//*[@id="tblnewAdd"]/tbody/tr[%s]/td[4]' % row).text 
        link = driver.find_element_by_xpath('//*[@id="tblnewAdd"]/tbody/tr[%s]/td[4]/a' % row)
        link.click()
        time.sleep(1)
        project_id_number = driver.find_element_by_xpath('//*[@id="projectInformationID"]').text
        environmental_category = driver.find_element_by_xpath('//*[@id="projectInformationCategory"]').text
        financial_institution = driver.find_element_by_xpath('//*[@id="projectInformationGrant"]').text
        try: 
            filers = driver.find_element_by_xpath('//*[@id="caseInformationRequesters"]/div/p').text
        except NoSuchElementException:
            filers = driver.find_element_by_id('caseInformationRequesters').text
        stages = driver.find_elements_by_xpath('//*[@id="CaseViewTabs"]/ul/li')
        stage_range = range(1, len(stages)+1)
        for stage in stage_range:
            each_stage = driver.find_element_by_xpath('//*[@id="CaseViewTabs"]/ul/li[%s]' % stage)
            stage_class = each_stage.get_attribute('class')
            stage_text = each_stage.text
            for i in stage_text:
                if stage_text == 'Notice of Receipt':
                    if stage_class in ('completedCurrent', 'completedCurrent active', 'liClassFirst completedCurrent'):
                        date_filed = 'Completed'
                    else: 
                        date_filed = None
                if stage_text == 'Registration of Request':
                    if stage_class in ('completedCurrent', 'completedCurrent active', 'liClassFirst completedCurrent'):
                        registration_start_date = 'Completed'
                        registration_end_date = 'Completed'
                    else: 
                        registration_start_date = None
                        registration_end_date = None
                if stage_text in ('Management Response', 'Eligibility Report'):
                    if stage_class in ('completedCurrent', 'completedCurrent active', 'liClassFirst completedCurrent'):
                        eligibility_start_date = 'Completed'
                    else: 
                        eligibility_start_date = None
                if stage_text == 'Board Approval':
                    if stage_class in ('completedCurrent', 'completedCurrent active', 'liClassFirst completedCurrent'):
                        eligibility_end_date = 'Completed'
                    else: 
                        eligibility_end_date = None
                if stage_text in ('Investigation Ongoing', 'Investigation Report', 'Management Report'):
                    if stage_class in ('completedCurrent', 'completedCurrent active', 'liClassFirst completedCurrent'):
                        cr_start_date = 'Completed'
                    else: 
                        cr_start_date = None
                if stage_text == 'Investigation Report':
                    if stage_class in ('completedCurrent', 'completedCurrent active', 'liClassFirst completedCurrent'):
                        cr_report = 'TRUE'
                    else: 
                        cr_report = 'FALSE'
                if stage_text == 'Board Discussion':
                    if stage_class in ('completedCurrent', 'completedCurrent active', 'liClassFirst completedCurrent'):
                        cr_end_date = 'Completed'
                    else: 
                        cr_end_date = None
                if stage_text == 'Follow up and Progress Report':
                    if stage_class in ('completedCurrent', 'completedCurrent active', 'liClassFirst completedCurrent'):
                        monitoring_start_date = 'Completed'
                        monitoring_end_date = 'Completed'
                    else: 
                        monitoring_start_date = None
                        monitoring_end_date = None
                if stage_text == 'Process Completed':
                    if stage_class in ('completedCurrent', 'completedCurrent active', 'liClassFirst completedCurrent'):
                        date_closed = 'Completed'
                        complaint_status = 'Closed'
                    else: 
                        date_closed = None
                        complaint_status = 'Open'
        documents_list = driver.find_elements_by_class_name('DocsList')
        for document in documents_list:
            attached_documents = document.find_element_by_css_selector('a').get_attribute('href')
        complaint_window = driver.window_handles[0]
        try: 
            project_link = driver.find_element_by_id('projectInformationTitle')
            project_link.click()
            time.sleep(2)
            project_window = driver.window_handles[1]
            driver.switch_to_window(project_window)
            project_details_link = driver.find_element_by_xpath('//*[@id="projdetailsId"]')
            project_details_link.click()
            time.sleep(4)
            try:
                print('we here!')
                project_company = driver.find_element_by_xpath('//*[@id="projectDetails"]/div[1]/div[2]/table/tbody/tr[3]/td[2]').text
                print('did this run?')
            except Exception as error:
                print('are we here?')
                print(error)
                project_company = 'None'
            project_loan = driver.find_element_by_xpath('//*[@id="projectDetails"]/div[1]/div[2]/table/tbody/tr[5]/td[2]').text
            sectors = driver.find_elements_by_xpath('//*[@id="projectDetails"]/div[2]/div[1]/div')
            sector_range = (1, len(sectors))
            sector_list = []
            for i in sector_range:
                sector = driver.find_element_by_xpath('//*[@id="projectDetails"]/div[2]/div[1]/div[%s]/div/div/div[1]' % i).text
                sector_list.append(sector)
            issues = driver.find_elements_by_xpath('//*[@id="accordion_theme"]/div')
            issue_range = range(1, len(issues)+1)
            issue_list = []
            for i in issue_range:
                issue = driver.find_element_by_xpath('//*[@id="accordion_theme"]/div[%s]/div[1]/span' % i).text
                issue_list.append(issue)
            driver.close()
            driver.switch_to_window(complaint_window)
        except Exception as error:
            print (error)
            print ('No project link')
        row_data = [
            'Panel',
            year,
            country,
            project,
            case_id,
            23,
            filers,
            environmental_category,
            project_company,
            project_id_number,
            None,
            None,
            financial_institution,
            project_loan,
            sector_list,
            issue_list,
            complaint_status,
            date_filed,
            registration_start_date,
            registration_end_date,
            eligibility_start_date,
            eligibility_end_date,
            None,
            None,
            cr_start_date,
            cr_end_date,
            monitoring_start_date,
            monitoring_end_date,
            date_closed,
            None,# attached_documents,
            driver.current_url,
            cr_report
        ]
        writer.writerow(row_data)
        print(row_data)
        time.sleep(0.25)
        driver.execute_script('window.history.go(-1)')
        time.sleep(2)
    return True
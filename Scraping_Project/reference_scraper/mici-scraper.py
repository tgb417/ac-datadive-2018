
# coding: utf-8

# # Scraper for the MICI website
# 

# In[ ]:


#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup
import pandas as pd


# In[ ]:


base_url = "https://idblegacy.iadb.org/en/mici/by-country,7631.html?status=&country=url.country&yearDate=&page="


# In[ ]:


def get_page_content(url):
    """
        Given a url, this would return the html content of the page parsed by BeautifulSoup
    """
    page = requests.get(url)
    page_content = BeautifulSoup(page.content, 'html.parser')
    return page_content


# In[ ]:


def get_last_page_number():
    """
        Finds the last page number in the pagination to help in navigation of projects
    """
    url = "https://idblegacy.iadb.org/en/mici/by-country,7631.html"
    page_content = get_page_content(url)
    return page_content.find('a',text='Last ')['href'].split('=')[-1]


# In[ ]:


def get_project_links(url):
    """
        Given a url, finds the links to projects listed in the page
        
    """
    page_content = get_page_content(url)
    search_results = page_content.find(id="searchResults")
    return search_results.find_all('li')


# In[ ]:


def get_project_name_and_id(link):
    """
        finds the project name and project ID from a project URL
        
        For example:
        link = <a href="/en/mici/complaint-detail,19172.html?ID=MICI-BID-BR-2018-0132" style="cursor:pointer;">
                    São José dos Campos Urban Structuring Program-Request II (MICI-BID-BR-2018-0132)
                </a>
        project name = São José dos Campos Urban Structuring Program-Request II
        project id = MICI-BID-BR-2018-0132
                    
    """
    project_link = link.find('a')
    project_link_text = project_link.getText()
    project_name = project_link_text.split("(")[0].strip()
    project_id = project_link_text.split("(")[1].replace(")","").strip()
    return project_name, project_id


# In[ ]:


def get_country_year_info(link):
    """
        given the project link, finds the country and year info from a div element inner to it.
        
        For example:
            <span class="smaller9 removeMarginBottom" style="width:345px; float:left;"> 
                Brazil - 2018 
            </span>
        country = Brazil
        year = 2018
        
    """
    div = link.find('div')
    country_year_info = div.find_all('span')[0].getText()
    return country_year_info.split("-")


# In[ ]:


def get_project_status(link):
    """
        given the project link, extracts the status info from it.
        
        for example:
            <span class="smaller9 removeMarginBottom" style="width:345px; float:left;">
                Status: <b>Closed</b> 
            </span>
        status = closed
    """
    div = link.find('div')
    status = div.find_all('span')[1].getText().split(":")[1].strip()
    return status


# In[ ]:


def get_detailed_project_url(link):
    """
        Generates the link to the individual project given the <a href></a> element
        For example:
            <a href="/en/mici/complaint-detail,19172.html?ID=MICI-BID-BR-2018-0132">
        
        returns: https://idblegacy.iadb.org/en/mici/complaint-detail,19172.html?ID=MICI-BID-BR-2018-0132
    """
    base_url = "https://idblegacy.iadb.org"
    href = link.find('a').get('href')
    return base_url + href
    


# In[ ]:


def get_additional_project_info(project_page):
    """
        From the project page, extract additional project information 
        For example:
        <div class="detailboxContent">
            <b>Project Number:</b>
            <p>BR-L1160</p> 
            <b>Environmental Category:</b> <p> B </p>
            <b> Project Name: </b> <p> São José dos Campos Urban Structuring Program </p>
            <b> Sector: </b> <p> URBAN DEVELOPMENT AND HOUSING </p> 
            <b> Project Type: </b> <p> Loan Operation </p> 
            <b> IDB Financing: </b> <p> USD 85,672,400 </p> 
        </div>
        
        From this we can extract additional info about the project such as Project Number, Environmental category etc.,
    """
    additional_project_info = {}
    try:
        detailed_project_content = project_page.find("div", {"class": "detailboxContent"})
        project_info_keys = [b.getText().strip() for b in detailed_project_content.find_all('b')]
        project_info_values = [p.getText().strip() for p in detailed_project_content.find_all('p')]
        additional_project_info = dict(zip(project_info_keys, project_info_values))
    except:
        pass
    return additional_project_info


# In[ ]:


def update_additional_project_info(additional_project_info, project_details):
    """
        Updates the project details object with the additional project information 
        got from the method "get_additional_project_info"
    """
    project_details["project_number"] = additional_project_info.get("Project Number:")
    project_details["environmental_category"] = additional_project_info.get("Environmental Category:")
    project_details["project_company"] = None
    project_details["Project Type:"] = additional_project_info.get("Project Type:")
    project_details["sector"] = additional_project_info.get("Sector:")
    project_details["issues"] = None
    project_details["financial_institution"] = None
    project_details["financing"] = additional_project_info.get("IDB Financing:")
    project_details["related_project_number"] = additional_project_info.get("Other related projects:")


# In[ ]:


def get_stage_names(project_year):
    """
        Returns the sub stages that project lifecycle is comprised. 
        It is modeled slightly different for project before and after 2014. 
        
        Example project before 2014:
        https://idblegacy.iadb.org/en/mici/complaint-detail-2014,1804.html?ID=ME-MICI002-2012
        
        Example project after 2014: 
        https://idblegacy.iadb.org/en/mici/complaint-detail,19172.html?ID=MICI-BID-BR-2018-0132
    """
    if project_year > 2014:
         return ["Registration", "Eligibility", "Assessment", "Consultation Phase", "DR-Monitoring", 
                      "Recommendation for a CR and ToRs", "Investigation", "CR Report", "CR-Monitoring"]
    else:
        return ["DR-Eligibility", "Assessment", "Consultation Phase Exercise", "DR-Monitoring", "CR-Eligibility",
                      "Preparation of TORs", "Investigation", "Panel Report", "CR-Monitoring"]
        


# In[ ]:


def get_project_stage_elements(project_year, project_page):
    """
        The html elements that have the project stage information is different for project before and after 2014.
        This method extracts the project stage related html elements based on the project year. 
    """
    project_stage_elements = []
    if project_year > 2014:
        project_stage_table = project_page.find("tr", {"class":"cuadro_dw_gris"})
        project_stage_elements = project_stage_table.find_all("td")
    else:
        project_stage_table = project_page.find("div", {"class": "tabla_principal"})
        project_stage_divs = project_stage_table.find_all("div")
        project_stage_elements = []
        for stage_div in project_stage_divs:
            if 'cuadro_up_' in stage_div.get('class')[0]:
                project_stage_elements.append(stage_div)
    return project_stage_elements
            
    


# In[ ]:


def get_completed_stage_css_class(project_year):
    """
        the css class of the html elements are the indicators that tell if the project stage has started/ended.
        This differs for projects before and after 2014. 
        This method returns the expected css class values for each project stage to know it it has started/ended
    """
    if project_year > 2014:
        return ["sltgray", "sltgray", "sltgreen", "sltgreen", "sltgreen", "cuadro_dw_azul",
                                     "cuadro_dw_azul", "cuadro_dw_azul", "cuadro_dw_azul"]
    else:
        return ["cuadro_up_ok" for i in xrange(9)]


# In[ ]:


def get_project_stages_current_state(project_year, project_page):
    """
        this method updates the state of every stage in the project by comparing the css class value of the stage with
        the expected css value.
    """
    project_stages_current_state = {}
    stage_names = get_stage_names(project_year)
    project_stage_elements = get_project_stage_elements(project_year, project_page)
    completed_stage_css_class = get_completed_stage_css_class(project_year)
    
    for i in xrange(len(project_stage_elements)):
        if completed_stage_css_class[i] in project_stage_elements[i].get('class'):
            project_stages_current_state[stage_names[i]] = True

    return project_stages_current_state


# In[ ]:


def update_stage_info(stage, start_date_key, end_date_key, project_stages_current_state, project_details):
    """
        updates the start end and end date completion for a given stage, 
        if project_stages_current_state has the corresponding start date / end date key is set to True
        
        For example:
        Dispute Resolution stage is said to be started when the project is in Assesment phase
        so, if "Assesment" is set to True in project_stages_current_state,
        project_details[dispute_resolution_start_date] will be set to "completed"
        
    """
    if project_stages_current_state.get(start_date_key):
        project_details[stage + "_start_date"] = "completed"
    if project_stages_current_state.get(end_date_key):
        project_details[stage + "_end_date"] = "completed"   
    


# In[ ]:


def update_project_stage_completion_info(project_year, project_stages_current_state, project_details):
    """
        There are 5 high level stages in a project, namely:
            1. Registration
            2. Eligibility
            3. Monitoring
            4. Dispute Resolution
            5. Compliance Review
            
            Based on the current state information obtained for each project stage, 
            we update if the start and end date has been completed for that stage. 
            
            This logic differs for projects before and after 2014 as we know the stages are named
            slightly different respectively. 
        
    """
    STAGE_COMPLETED = "completed"
    project_stage_completetion_info = {}
    
    if project_year > 2014:
        update_stage_info("registration", "Registration",  "Eligibility", project_stages_current_state, project_details)
        update_stage_info("eligibility", "Eligibility",  "", project_stages_current_state, project_details)
        update_stage_info("monitoring", "",  "DR-Monitoring", project_stages_current_state, project_details)
        update_stage_info("monitoring", "",  "CR-Monitoring", project_stages_current_state, project_details)
        update_stage_info("dispute_resolution", "Assessment",  "Consultation Phase", project_stages_current_state, project_details)
        update_stage_info("compliance_review", "Recommendation for a CR and ToRs",  "CR Report", project_stages_current_state, project_details)
        
        if project_details["status"] == "closed":
            project_stage_completetion_info["monitoring_end_date"] = STAGE_COMPLETED
    else:
        update_stage_info("registration", "",  "", project_stages_current_state, project_details)
        update_stage_info("eligibility", "",  "DR-Eligibility", project_stages_current_state, project_details)
        update_stage_info("eligibility", "",  "CR-Eligibility", project_stages_current_state, project_details)
        update_stage_info("monitoring", "",  "DR-Monitoring", project_stages_current_state, project_details)
        update_stage_info("monitoring", "",  "CR-Monitoring", project_stages_current_state, project_details)
        update_stage_info("dispute_resolution", "Assessment",  "Consultation Phase Exercise", project_stages_current_state, project_details)
        update_stage_info("compliance_review", "Preparation of TORs",  "Panel Report", project_stages_current_state, project_details)
    
    
    return project_stage_completetion_info
        
    


# In[ ]:


project_list = []
last_page_number = int(get_last_page_number())

for page_number in xrange(1, last_page_number):
    
    url = base_url + str(page_number)
    
    project_links = get_project_links(url)

    for link in project_links:
        project_details = {}

        # update IAM info
        project_details["IAM"] = "MICI"
        project_details["IAM_id"] = 24

        # update project name, id info
        project_details["project_name"], project_details["project_id"]  = get_project_name_and_id(link)

        # update country, year info
        project_details["country"], project_details["year"] = get_country_year_info(link)
        
        print "scraping project details for:"
        print project_details["project_name"]
        print project_details["country"], project_details["year"]
        
        # hack 
        if project_details["project_id"] == "MICI-AR-2015-0084":
            project_details["year"] = 2015

        # update Status
        project_details["status"] = get_project_status(link)

        # TODO: update filer info

        project_url = get_detailed_project_url(link)
        
        # update detailed project link
        project_details["Hyperlink"] = project_url
        
        # fetching and updating additional project info from the project page
        project_page = get_page_content(project_url)
        additional_project_info = get_additional_project_info(project_page)
        update_additional_project_info(additional_project_info, project_details)

        # fetching and updating start / end date completion for every stage of the project
        project_stages_current_state = get_project_stages_current_state(int(project_details["year"]), project_page)
        update_project_stage_completion_info(project_details["year"], project_stages_current_state, project_details)

        project_details["Date Closed"] = "completed" if project_details["status"] =="Closed" else None
        
        # TODO
        project_details["Documents"] = None
        
        project_list.append(project_details)
        
        print "************************************************************************************"
        


    


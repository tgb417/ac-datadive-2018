
from datamodel import Fields
from collections import OrderedDict


def get_complete_project_row(project_details):
    """
        Given a dictionary with the scraped information about a project, 
        this util method creates a ordered dictionary with values,
            if present in project_details else as None
            
        This can be useful to store consistent set of fields for all scraped projects
    """
    project_row = OrderedDict()
    for field in list(Fields):
        project_row[field] = project_details.get(field)
    return project_row


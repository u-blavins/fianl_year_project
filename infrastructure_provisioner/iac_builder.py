import json


class iac_builder:
    """ Class that builds CloudFormation templates """

    def __init__(self):
        """ Initialise Class """
        self.template = {
            'AWSTemplateFormatVersion': '2010-09-09',
            'Description': '',
            'Resources': {}
        }
    
    def add_resource(self, resource):
        """ Method that add a resource to CloudFormation """
        return

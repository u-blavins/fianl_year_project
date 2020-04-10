import json


class CF_BUILDER:
    """ Class that builds CloudFormation templates """

    def __init__(self):
        """ Initialise Class """
        self.resources = {}
        self.cft = {
            'AWSTemplateFormatVersion': "2010-09-09",
            'Description': '',
            'Resources': self.resources
        }
        self.types = {
            'S3Bucket': {
                'Resource': 'Bucket',
                'Type': 'AWS::S3::Bucket'
            },
            'S3BucketPolicy': {
                'Resource': 'BucketPolicy',
                'Type': 'AWS::S3::BucketPolicy'
            }
        }

    def set_description(self, desc):
        """ Set the description of the CloudFormation Template """
        self.cft['Description'] = desc

    def get_description(self):
        """ Get the description of the CloudFormation Template """
        return self.description

    def set_resources(self, resource_type, resource):
        """ Set the resource and type """
        if resource_type in self.types:
            res_type = self.types[resource_type]
            self.resources[res_type['Resource']] = {
                'Type': res_type['Type'],
                'Properties': resource
            }
    
    def get_resources(self):
        """ Get the resources of the CloudFormation Template """
        return self.resources

    def get_template(self):
        """ Get the constructed CloudFormation Template """
        return self.cft

import json
from copy import deepcopy


class GOVERNANCE:
    """ Class for applying governance to CloudFormation Templates """

    def __init__(self, template={}):
        """ Instantiate Object """
        self.resource_types = {
            'AWS::S3::Bucket': 'S3',
            'AWS::S3::BucketPolicy': 'S3' 
        }
        self.template = template
        self.resources = {}
        self.get_all_resources()
        self.governance_handler()

    def get_resources(self):
        """ Getter for resources within a CloudFormation Template """
        return self.resources

    def get_all_resources(self):
        """ Get all the resources within a CloudFormation Template """
        if 'Resources' in self.template:
            resources = self.template['Resources']
            for resource in resources:
                if 'Type' in resources[resource]:
                    self.set_resources(
                        resources[resource]['Type'],
                        resources[resource]['Properties'])
    
    def set_resources(self, resource_type, res_property):
        """ Validates if resource type is valid """
        if resource_type in self.resource_types:
            if resource_type not in self.resources:
                self.resources[resource_type] = res_property
            
    def governance_handler(self):
        """ Handles reources to perform governance checks """
        for resource in self.resources.keys():
            if self.resource_types[resource] == 'S3':
                s3_governance = S3_GOVERNANCE(
                    resource, self.resources[resource])
                s3_governance.s3_handler()


class S3_GOVERNANCE:
    """ Class that governs S3 resource types """
    
    def __init__(self, res_type, res_property):
        self.res_type = res_type
        self.res_property = res_property
        self.rules = self.load_rules()

    def s3_handler(self):
        """ Handles S3 resource types for applying governance to """
        if self.res_type == 'AWS::S3::Bucket':
            self.s3_bucket_governance()

    def s3_bucket_governance(self):
        """ Govern S3 Bucket properties """
        for rule in self.rules.keys():
            props = self.rules[rule]
            if rule == 'BucketEncryption':
                self.bucket_encryption(props)
            if rule == 'VersioningConfiguration':
                self.version_configuration(props)
            if rule == 'PublicAccessBlockConfiguration':
                self.public_access(props)
            if rule == 'AccessControl':
                self.access_control(props)

    def bucket_encryption(self, props):
        """ Method that governs bucket encryption configuration 
        
        Args:
            props (dict): governance properties
        """
        encryption_rule = \
            props['ServerSideEncryptionConfiguration'][0]\
            ['ServerSideEncryptionByDefault']
        
        mandatory = encryption_rule['Mandatory']
        accepted = encryption_rule['Accepted']
        
        if 'BucketEncryption' in self.res_property:
            encryption = \
                self.res_property['BucketEncryption']\
                ['ServerSideEncryptionConfiguration'][0]\
                ['ServerSideEncryptionByDefault']

            if encryption != mandatory and encryption != accepted:
                self.res_property['BucketEncryption'] = {
                    'ServerSideEncryptionConfiguration': [
                        {'ServerSideEncryptionByDefault': mandatory}]}
        else:
            self.res_property['BucketEncryption'] = {
                'ServerSideEncryptionConfiguration': [
                    {'ServerSideEncryptionByDefault': mandatory}]}

    def load_rules(self):
        """ Load Governance policies """
        rules = {}
        with open('rules.json') as file:
            rules = json.load(file)
        return rules

    def get_rules(self):
        """ Getter for governance rules """
        return self.rules

def main():
    """ Main Function for local testing """

    test_template = {
        "Resources": {
            "Bucket": {
                "Type": "AWS::S3::Bucket",
                "Properties": {
                    "BucketName": "test-bucket",
                    "BucketEncryption": {
                        "ServerSideEncryptionConfiguration": [
                            {
                                "ServerSideEncryptionByDefault": {
                                    "Test": "Test"
                                }
                            }
                        ]
                    }
                }
            }
        }
    }

    before = deepcopy(test_template)
    governance = GOVERNANCE(template=test_template)
    print(json.dumps(before, indent=4))
    print(json.dumps(test_template, indent=4))

main()
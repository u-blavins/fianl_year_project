import boto3
import json


class S3:
    """ Class for the Simple Storage Service """

    def __init__(self, region='eu-west-2'):
        """ Initialise Object """
        self.client = boto3.client(
            service_name='s3', region_name=region)

    def backup_cloudformation_temlates(self, template, region='eu-west-2'):
        """ Method that backs a CloudFormation Template to S3 """
        regions = {
            'eu-west-1': 'euw1',
            'eu-west-2': 'euw2'
        }
        backup_bucket = 'cft-bucket-{}'.format(regions[region])
        bucket_name = self.get_bucket_from_cloudformation_template(template)
        key = '{}/{}.json'.format(region, bucket_name)

        if template != {}:
            response = self.client.put_object(
                Body=json.dumps(template),
                Bucket=backup_bucket,
                Key=key
            )
            return response

    @staticmethod
    def get_bucket_from_cloudformation_template(template):
        """ Method that extracts bcuekt name from a CloudFormation Template """
        if 'Resources' in template:
            resources = template['Resources']
            for resource in resources.keys():
                if resources[resource]['Type'] == 'AWS::S3::Bucket':
                    properties = resources[resource]['Properties']
                    if 'BucketName' in properties:
                        return properties['BucketName']
        return

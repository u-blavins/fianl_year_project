import json

class S3_CF:
    """Class that converts s3 payload into CloudFormation"""

    def __init__(self, template, payload):
        self.payload = payload
        self.template = template
        self.S3_BUCKET_PROPERTIES = {
            "AccelerationConfiguration": self.get_acceleration_config(
                self.payload, "AccelerationConfiguration"),
            "AccessContol": self.get_access_control(
                self.payload, "AccessControl"),
            "AnalyticsConfiguration": self.get_analytics_configuration(
                self.payload, "AnalyticsConfiguration"),
            "BucketEncryption": 0,
            "BucketName": 0,
            "CorsConfiguration": 0,
            "InventoryConfigurations": 0,
            "LifecycleConfiguration": 0,
            "LoggingConfiguration": 0,
            "MetricsConfigurations": 0,
            "NotificationConfiguration": 0,
            "ObjectLockConfiguration": 0,
            "PublicAccessConfiguration": 0,
            "ReplicationConfiguration": 0,
            "Tags": 0,
            "VersionConfiguration": 0,
            "WebsiteCOnfigration": 0
        }
        self.construct_template()
    
    def construct_tags(self, tags):
        """ Method that returns cloud formation friendly tags"""
        cf_tags = []
        for tag in tags:
            temp={}
            temp['Key']   = tag
            temp['Value'] = tags[tag]
            cf_tags.append(temp)
        return cf_tags


    def construct_template(self):
        """ Method that constructs IAC template from payload """
        for bucket_property in self.payload.keys():
            print(bucket_property)
            if bucket_property in self.S3_BUCKET_PROPERTIES:
                self.S3_BUCKET_PROPERTIES[bucket_property]
    
    def get_acceleration_config(self, payload, arg):
        """ Method that checks acceleration configuration from payload """
        accepted_options = [
            "Enabled",
            "Suspended"
        ]
        bucket_property = payload[arg]
        if isinstance(bucket_property, str):
            if bucket_property in accepted_options:
                self.template[arg] = {
                    arg: bucket_property
                }

    def get_access_control(self, payload, arg):
        """ Method that checks access control configuration from payload """
        accepted_options = [
            "private", "public-read", "public-read-write",
            "aws-exec-read", "authenticated-read", "bucket-owner-read",
            "bucket-owner-full-control", "log-delivery-write"
        ]
        bucket_property = payload[arg]
        if isinstance(bucket_property, str):
            if bucket_property in accepted_options:
                template[arg] = bucket_property
    
    def get_analytics_configuration(self, payload, arg):
        """ Method that checks analytics configuration from payload """
        template = {}
        bucket_property = payload[arg]
        if isinstance(bucket_property, dict):
            if "Id" in bucket_property:
                template['Id'] = bucket_property['Id']
            if "Prefix" in bucket_property:
                template['Prefix'] = bucket_property['Prefix']
            if "Destination" in bucket_property:
                "do something here"
            if "TagFilters" in bucket_property:
                template['TagFilters'] = self.construct_tags(
                    bucket_property['TagFilters'])
                

    def get_iac_template(self):
        """ Method that returns iac template from configuration options """
        return self.template

def main():
    payload = {
        "AnalyticsConfiguration": {
            "Id": "test",
            "Prefix": "test",
            "TagFilters": [
                {
                    "temp": "temp"
                },
                {
                    "temp1": "test"
                }
            ]
        }
    }
    temp = {}
    test = S3_CF(temp, payload)
    print(json.dumps(test.get_iac_template(), indent=2))
    
main()
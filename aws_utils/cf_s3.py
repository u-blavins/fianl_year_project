import json

class S3_CF:
    """Class that converts s3 payload into CloudFormation"""

    def __init__(self, payload):
        self.payload = payload
        self.template = {}
        self.S3_BUCKET_PROPERTIES = [
            "AccelerationConfiguration",
            "AccessContol",
            "AnalyticsConfiguration",
            "BucketEncryption",
            "BucketName",
            "CorsConfiguration",
            "InventoryConfigurations",
            "LifecycleConfiguration",
            "LoggingConfiguration",
            "MetricsConfigurations",
            "NotificationConfiguration",
            "ObjectLockConfiguration",
            "PublicAccessConfiguration",
            "ReplicationConfiguration",
            "Tags",
            "VersionConfiguration",
            "WebsiteCOnfigration"
        ]
        self.construct_template()
    
    def construct_tags(self, tags):
        """ Method that returns cloud formation friendly tags"""
        cf_tags = []
        for tag in tags:
            temp={}
            key = list(tag.keys())[0]
            temp['Key']   = key
            temp['Value'] = tag[key]
            cf_tags.append(temp)
        return cf_tags

    def method_handler(self, arg):
        """ Method that handles different method calls """
        if arg == "AccelerationConfiguration":
            self.get_acceleration_config(arg)
        elif arg == "AccessControl":
            self.get_access_control(arg)
        elif arg == "AnalyticsConfiguration":
            self.get_analytics_configuration(arg)

    def construct_template(self):
        """ Method that constructs IAC template from payload """
        for bucket_property in self.payload.keys():
            if bucket_property in self.S3_BUCKET_PROPERTIES:
                self.method_handler(bucket_property)
    
    def get_acceleration_config(self, arg):
        """ Method that checks acceleration configuration from payload """
        accepted_options = [
            "Enabled",
            "Suspended"
        ]
        bucket_property = self.payload[arg]
        if isinstance(bucket_property, str):
            if bucket_property in accepted_options:
                self.template[arg] = {
                    arg: bucket_property
                    }

    def get_access_control(self, arg):
        """ Method that checks access control configuration from payload """
        accepted_options = [
            "private", "public-read", "public-read-write",
            "aws-exec-read", "authenticated-read", "bucket-owner-read",
            "bucket-owner-full-control", "log-delivery-write"
        ]
        bucket_property = self.payload[arg]
        if isinstance(bucket_property, str):
            if bucket_property in accepted_options:
                template[arg] = bucket_property
    
    def get_analytics_configuration(self, arg):
        """ Method that checks analytics configuration from payload """
        template = {}
        bucket_property = self.payload[arg]
        if isinstance(bucket_property, dict):
            if "Id" in bucket_property:
                template['Id'] = bucket_property['Id']
            if "Prefix" in bucket_property:
                template['Prefix'] = bucket_property['Prefix']
            if "Destination" in bucket_property:
                print("do something")
            if "TagFilters" in bucket_property:
                template['TagFilters'] = self.construct_tags(
                    bucket_property['TagFilters'])
        self.template[arg] = template
                

    def get_iac_template(self):
        """ Method that returns iac template from configuration options """
        return self.template

def main():
    payload = {
        "AnalyticsConfiguration": {
            "Id": "test",
            "Prefix": "test",
            "Destination": "test",
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
    test = S3_CF(payload)
    print(json.dumps(test.get_iac_template(), indent=2))
    
main()
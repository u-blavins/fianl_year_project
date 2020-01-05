import json

class S3_CF:
    """Class that converts s3 payload into CloudFormation"""

    def __init__(self, template, payload):
        self.payload = payload
        self.template = template
        self.S3_BUCKET_PROPERTIES = {
            "AccelerationConfiguration": self.get_acceleration_config(),
            "AccessContol": self.get_access_control(),
            "AnalyticsConfiguration": 0,
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
        

    def construct_template(self):
        """ Method that constructs IAC template from payload """
        for bucket_property in self.payload.keys():
            if bucket_property in self.S3_BUCKET_PROPERTIES:
                self.S3_BUCKET_PROPERTIES[bucket_property]
    
    def get_acceleration_config(self):
        """ Method that checks acceleration configuration from payload """
        accepted_options = [
            "Enabled",
            "Suspended"
        ]
        bucket_property = self.payload['AccelerationConfiguration']
        if isinstance(bucket_property, str):
            if bucket_property in accepted_options:
                self.template['AccelerationConfiguration'] = {
                    "AccelerationStatus": bucket_property
                }

    def get_access_control(self):
        """ Method that checks access control configuration from payload """
        accepted_options = [
            "private", "public-read", "public-read-write",
            "aws-exec-read", "authenticated-read", "bucket-owner-read",
            "bucket-owner-full-control", "log-delivery-write"
        ]
        bucket_property = self.payload['AccessControl']
        if isinstance(bucket_property, str):
            if bucket_property in accepted_options:
                template['AccessControl'] = bucket_property
    
    def get_analytics_configuration(self):
        """ Method that checks analytics configuration from payload """
        

    def get_iac_template(self):
        """ Method that returns iac template from configuration options """
        return self.template

    
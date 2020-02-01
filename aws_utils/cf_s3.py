import json

class S3_CF:
    """Class that converts s3 payload into CloudFormation"""

    def __init__(self, payload):
        self.payload = payload
        self.template = {}
        self.response = {}
        self.S3_BUCKET_PROPERTIES = [
            "AccelerateConfiguration",
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
        """ Method that returns cloud formation friendly tags """
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
        if arg == "AccelerateConfiguration":
            self.get_acceleration_config(arg)
        if arg == "AccessControl":
            self.get_access_control(arg)
        if arg == "AnalyticsConfiguration":
            self.get_analytics_configuration(arg)
        if arg == "BucketEncryption":
            self.get_bucket_encryption(arg)
        if arg == "CorsConfiguration":
            self.get_cors_configuration(arg)
        if arg == "VersionConfiguration":
            self.get_version_configuration(arg)

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
                        "AccelerationStatus": bucket_property
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
        dest = {}
        analytics_properties = ["Id", "Prefix", "Destination", "TagFilters"]
        bucket_property = self.payload[arg]
        if isinstance(bucket_property, dict):
            for prop in bucket_property:
                if prop in analytics_properties:
                    if prop == "Destination":
                        if "BucketAccountId" in bucket_property[prop]:
                            dest['BucketAccountId'] = \
                                bucket_property[prop]['BucketAccountId']
                        if "Prefix" in bucket_property[prop]:
                            dest['Prefix'] = bucket_property[prop]['Prefix']
                        if "BucketArn" in bucket_property[prop]:
                            dest['BucketArn'] = \
                                bucket_property[prop]['BucketArn']
                            dest['Format'] = "CSV"
                            template['StorageClassAnalysis'] = {
                                "DataExport": dest,
                                "OutputSchemaVersion": "V_1"
                            }
                    elif prop == "TagFilters":
                        template[prop] = self.construct_tags(
                            bucket_property[prop]
                        )
                    else:
                        template[prop] = bucket_property[prop]
        if "StorageClassAnalysis" in template:
            self.template[arg] = template

    def get_bucket_encryption(self, arg):
        """ Method that checks bucket encryption from payload """
        encryption = {}
        bucket_property = self.payload[arg]
        if isinstance(bucket_property, dict):
            if "SSEAlgorithm" in bucket_property:
                if bucket_property['SSEAlgorithm'] == "aws:kms":
                    if "KMSMasterKeyID" in bucket_property:
                        encryption = {
                            "SSEAlgorithm": bucket_property["SSEAlgorithm"],
                            "KMSMasterKeyID": bucket_property['KMSMasterKeyID'] 
                        }
                elif bucket_property['SSEAlgorithm'] == "AES256":
                    encryption = {
                        "SSEAlgorithm": bucket_property["SSEAlgorithm"]}
        if "SSEAlgorithm" in encryption:
            self.template[arg] = {
                "ServerSideEncryptionConfiguration": {
                    "ServerSideEncryptionByDefault": encryption
                }
            }
    
    def get_cors_configuration(self, arg):
        """ Method that checks cors configuration from payload """
        corsrules = []
        allowed_methods = ['GET', 'PUT', 'HEAD', 'POST', 'DELTE']
        bucket_property = self.payload[arg]
        for configuration in bucket_property:
            corsrule = {}
            if "AllowedHeaders" in configuration:
                if isinstance(configuration['AllowedHeaders'], list):
                    corsrule['AllowedHeaders'] = configuration['AllowedHeaders']
            if "AllowedMethods" in configuration:
                methods = []
                for method in configuration['AllowedMethods']:
                    if method in allowed_methods:
                        methods.append(method)
                corsrule['AllowedMethods'] = methods
            if "AllowedOrigins" in configuration:
                if isinstance(configuration['AllowedOrigins'], list):
                    corsrule['AllowedOrigins'] = configuration['AllowedOrigins']
            if "ExposedHeaders" in configuration:
                if isinstance(configuration['ExposedHeaders'], list):
                    corsule['ExposedHeaders'] = configuration['ExposedHeaders']
            if "Id" in configuration:
                if configuration["Id"] != "":
                    corsrule['Id'] = configuration['Id']
            if "MaxAge" in configuration:
                if isinstance(configuration['MaxAge'], int):
                    corsrule['MaxAge'] = configuration['MaxAge']
            if ("AllowedMethods" in corsrule) and ("AllowedOrigins" in corsrule):
                corsrules.append(corsrule)
        self.template[arg] = {
            "CorsRules": corsrules
        }

    def get_inventory_configuration(self, arg):
        """ Method that checks inventory configuration from payload """
        fields = [
            "Size", "LastModifiedDate", "StorageClass", "ETag", "IsMultiPartUpload",
            "ReplicationStatus", "EncryptionStatus", "ObjectLockRetainUntilDate",
            "ObjectLockMode", "ObjectLockLegalHoldStatus", "IntelligentTieringAccessTier"
        ]
        inventory_configurations = []
        bucket_property = self.payload[arg]
        for configuration in bucket_property:
            invetory = {}
            if "Destination" in configuration:
                dest = configuration['Destination']
                destination = {}
                if "BucketAccountId" in dest:
                    destination['BucketAccountId'] = dest['BucketAccountId']
                if "Prefix" in dest:
                    destination['Prefix'] = dest['Prefix']
                if "BucketArn" in dest:
                    destination['BucketArn'] = dest['BucketArn']
                    inventory['Destination'] = destination
            if "Enabled" in configuration:
                if configuration['Enabled'] in ['True', 'False']:
                    inventory['Enabled'] = configuration['Enabled']
            if "Id" in configuration:
                inventory['Id'] = configuration['Id']
            if "IncludeObjectVersions" in configuration:
                if configuration['IncludeObjectVersions'] in ['All', 'Current']:
                    inventory['IncludeObjectVersions'] = configuration['IncludeObjectVersions']
            if "OptionalFields" in configuration:
                fields = configuration['OptionalFields']


    
    def get_version_configuration(self, arg):
        """ Method that checks version configuration from payload """
        bucket_property =  self.payload[arg]
        if bucket_property in ['Enabled', 'Suspended']:
            self.template[arg] = bucket_property

    def get_iac_template(self):
        """ Method that returns iac template from configuration options """
        return self.template

def main():
    payload = {
        "AccelerateConfiguration": "Enabled",
        "AnalyticsConfiguration": {
            "Id": "test",
            "Prefix": "test",
            "Destination": {
                "BucketArn": "testarn"
            },
            "TagFilters": [
                {
                    "temp": "temp"
                },
                {
                    "temp1": "test"
                }
            ]
        },
        "BucketEncryption": {
            "SSEAlgorithm": "aws:kms",
            "KMSMasterKeyID": "testarn"
        },
        "CorsConfiguration": [
            {
                "AllowedHeaders": [
                    'test',
                    'test1'
                ],
                "AllowedMethods": [
                    'GET',
                    'POST',
                    'DELETE'
                ],
                "AllowedOrigins": [
                    'testorigin',
                    'testorigin1'
                ],
                "ExposedOrigins": [
                    'testexpheaders',
                    'testexpheaders1'
                ],
                "Id": 'testid',
                "MaxAge": 343
            },
            {
                "AllowedMethods": [
                    "GET",
                    "TEST"
                ],
                "AllowedOrigins": [
                    "testorigins"
                ]
            },
            {
                "AllowedMethods": "GET"
            }
        ],
        "VersionConfiguration": "Enabled"
    }
    test = S3_CF(payload)
    print(json.dumps(test.get_iac_template(), indent=2))
    
main()
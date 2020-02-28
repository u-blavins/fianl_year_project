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
        for key in tags.keys():
            temp={}
            temp['Key']   = key
            temp['Value'] = tags[key]
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
        if arg == "InventoryConfigurations":
            self.get_inventory_configuration(arg)
        if arg == "LifecycleConfiguration":
            self.get_lifecycle_configuration(arg)
        if arg == "LoggingConfiguration":
            self.get_logging_configuration(arg)
        if arg == "MetricsConfigurations":
            self.get_metrics_configuration(arg)
        if arg == "NotificationConfigrations":
            self.get_notification_configuration(arg)

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
        valid_fields = [
            "Size", "LastModifiedDate", "StorageClass", "ETag", "IsMultiPartUpload",
            "ReplicationStatus", "EncryptionStatus", "ObjectLockRetainUntilDate",
            "ObjectLockMode", "ObjectLockLegalHoldStatus", "IntelligentTieringAccessTier"
        ]
        inventory_configurations = []
        bucket_property = self.payload[arg]
        for configuration in bucket_property:
            inventory = {}
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
            if "OptionalFields" in configuration:
                opt_fields = []
                fields = configuration['OptionalFields']
                for field in fields:
                    if field in valid_fields:
                        opt_fields.append(field)
                if len(opt_fields) != 0:
                    inventory['OptionalFields'] = opt_fields
            if "Prefix" in configuration:
                inventory['Prefix'] = configuration['Prefix']
            if "Enabled" in configuration:
                if configuration['Enabled'] in ['True', 'False']:
                    inventory['Enabled'] = configuration['Enabled']
            if "Id" in configuration:
                inventory['Id'] = configuration['Id']
            if "IncludedObjectVersions" in configuration:
                if configuration['IncludedObjectVersions'] in ['All', 'Current']:
                    inventory['IncludedObjectVersions'] = configuration['IncludedObjectVersions']
            if "ScheduledFrequency" in configuration:
                if configuration['ScheduledFrequency'] in ['Daily', 'Weekly']:
                    inventory['ScheduledFrequency'] = configuration['ScheduledFrequency']
            if set(['Enabled', 'Id', 'IncludedObjectVersions', 'ScheduledFrequency']).issubset(set(inventory.keys())):
                inventory_configurations.append(inventory)
        if len(inventory_configurations) != 0:
            self.template[arg] = inventory_configurations

    def get_lifecycle_configuration(self, arg):
        """ Method that checks lifecycle configuration from payload """
        bucket_property = self.payload[arg]
        storage_class = [
            'DEEP_ARCHIVE', 'GLACIER', 'INTELLIGENT_TIERING', 'ONEZONE_IA', 'STANDARD_IA'
        ]
        optional_properties = [
            'AbortIncompleteMultipartUpload', 'ExpirationDate', 'ExpirationInDays',
            'NoncurrentVersionExpirationInDays', 'NoncurrentVersionTransitions',
            'Transitions'
        ]
        lifecycles = []
        for configuration in bucket_property:
            lifecycle = {}
            if "AbortIncompleteMultipartUpload" in configuration:
                days = configuration['AbortIncompleteMultipartUpload']
                if isinstance(days, int):
                    lifecycle['AbortIncompleteMultipartUpload'] = {
                        'DaysAfterInitiation': days }
            if "ExpirationDate" in configuration:
                lifecycle['ExpirationDate'] = configuration['ExpirationDate']
            if "ExpirationInDays" in configuration:
                expiration = configuration['ExpirationInDays']
                if isinstance(expiration, int):
                    lifecycle['ExpirationInDays'] = expiration
            if "NoncurrentVersionExpirationInDays" in configuration:
                expiration = configuration['NoncurrentVersionExpirationInDays']
                if isinstance(expiration, int):
                    lifecycle['NoncurrentVersionExpirationInDays'] = expiration
            if "NoncurrentVersionTransitions" in configuration:
                non_curr = []
                non_transitions = configuration['NoncurrentVersionTransitions']
                if isinstance(non_transitions, list):
                    for transition in non_transitions:
                        if 'StorageClass' in transition and 'TransitionInDays' in transition:
                            if transition['StorageClass'] in storage_class and \
                                isinstance(transition['TransitionInDays'], int):
                                non_curr.append({
                                    'StorageClass': transition['StorageClass'],
                                    'TransitionInDays': transition['TransitionInDays']
                                })
                if len(non_curr) != 0:
                    lifecycle['NoncurrentVersionTransitions'] = non_curr
            if 'Transitions' in configuration:
                transitions = []
                if isinstance(configuration['Transitions'], list):
                    for transition in configuration['Transitions']:
                        trans = {}
                        if "StorageClass" in transition:
                            if transition['StorageClass'] in storage_class:
                                trans['StorageClass'] = transition['StorageClass']
                        if "TransitionDate" in transition:
                            trans['TransitionDate'] = transition['TransitionDate']
                        if "TransitionInDays" in transition:
                            trans['TransitionInDays'] = transition['TransitionInDays']
                        if 'StorageClass' in trans:
                            if 'TransitionInDays' in trans or 'TransitionDate' in trans:
                                transitions.append(trans)
                if len(transitions) != 0:
                    lifecycle['Transitions'] = transitions
            if "Id" in configuration:
                lifecycle['Id'] = configuration['Id']
            if "Prefix" in configuration:
                lifecycle['Prefix'] = configuration['Prefix']
            if "Status" in configuration:
                if configuration['Status'] in ['Enabled', 'Disabled']:
                    lifecycle['Status'] = configuration['Status']
            if 'TagFilters' in configuration:
                lifecycle['TagFilters'] = self.construct_tags(
                    configuration['TagFilters'])
            if 'Status' in lifecycle:
                if 'AbortIncompleteMultipartUpload' in lifecycle or \
                    'ExpirationDate' in lifecycle or \
                    'ExpirationInDays' in lifecycle or \
                    'NoncurrentVersionExpirationInDays' in lifecycle or \
                    'NoncurrentVersionTransitions' in lifecycle or \
                    'Transitions' in lifecycle:
                    lifecycles.append(lifecycle)
        if len(lifecycles) != 0:
            self.template[arg] = {'Rules': lifecycles}
    
    def get_version_configuration(self, arg):
        """ Method that checks version configuration from payload """
        bucket_property = self.payload[arg]
        if bucket_property in ['Enabled', 'Suspended']:
            self.template[arg] = bucket_property

    def get_logging_configuration(self, arg):
        """ Method that checks logging configuration from payload """
        logging = {}
        bucket_property = self.payload[arg]
        if 'LogFilePrefix' in bucket_property:
            logging['LogFilePrefix'] = bucket_property['LogFilePrefix']
        if 'DestinationBucketName' in bucket_property:
            logging['DestinationBucketName'] = bucket_property['DestinationBucketName']
        if len(logging.keys()) != 0:
            self.template[arg] = logging

    def get_metrics_configuration(self, arg):
        """ Method that checks metric configuration from payload """
        metrics = []
        bucket_property = self.payload[arg]
        for configuration in bucket_property:
            metric = {}
            if 'Prefix' in configuration:
                metric['Prefix'] = configuration['Prefix']
            if 'TagFilters' in configuration:
                metric['TagFilters'] = self.construct_tags(
                    configuration['TagFilters'])
            if 'Id' in configuration:
                metric['Id'] = configuration['Id']
                metrics.append(metric)
        if len(metrics) != 0:
            self.template[arg] = metrics

    @staticmethod
    def get_notification(notification, config):
        """ Method that returns notification configations """
        notifications = []
        for configuration in conifg:
            notification = {}
            if 'Event' in configuration:
                notification['Event'] = configuration['Event']
            if 'Filter' in configuration:
                filters = []
                for filter in configuration['Filter']:
                    if 'Name' in filter and 'Value' in filter:
                        if filter['Name'] in ['prefix', 'suffix']:
                            filters.append(
                                {
                                    'Name': filter['Name'],
                                    'Value': filter['Value']
                                }
                            )


    def get_notification_configation(self, arg):
        """ Method that checks notification configuration from payload """
        notification = {}
        bucket_property = self.payload[arg]
        if 'LambdaConfigurations' in bucket_property:
            config = self.get_notification(
                'LambdaConfigurations', bucket_property['LambdaConfigurations'])
            if len(config) != 0:
                notification['LambdaConfigurations'] = config
        if 'QueueConfigurations' in bucket_property:
            config = self.get_notification(
                'QueueConfigurations', bucket_property['QueueConfigurations'])
            if len(config) != 0:
                notification['QueueConfigurations'] = config
        if 'TopicConfigurations' in bucket_property:
            config = self.get_notification(
                'TopicConfigurations', bucket_property['TopicConfigurations'])
            if len(config) != 0:
                notification['TopicConfigurations'] = config 
        if len(notification.keys()) != 0:
            self.template[arg] = notification 

    def get_iac_template(self):
        """ Method that returns iac template from configuration options """
        return self.template

def main():
    payload = {
        'LoggingConfiguration': {
            'DestinationBucketName': 'test',
            'LogFilePrefix': 'test2'
        },
        'MetricsConfigurations': [
            {
                "Id": "test",
                "Prefix": "~"
            },
            {
                "TagFilters": {
                    'key': 'value'
                },
                "Prefix": "~",
                "Id": "test"
            }
        ]
    }
    test = S3_CF(payload)
    print(json.dumps(test.get_iac_template(), indent=4))

main()
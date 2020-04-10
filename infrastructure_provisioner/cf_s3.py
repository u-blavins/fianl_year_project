from utils.response import ok
from utils.response import not_found


class S3_CF:
    """Class that converts s3 payload into CloudFormation"""

    def __init__(self, payload):
        self.payload = payload
        self.template = {}
        self.response = {}
        self.S3_BUCKET_PROPERTIES = [
            "AccelerateConfiguration",
            "AccessControl",
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
            "PublicAccessBlockConfiguration",
            "ReplicationConfiguration",
            "Tags",
            "VersioningConfiguration",
            "WebsiteConfiguration"
        ]

    def set_payload(self, payload):
        """ Setter for payload attribute

        Args:
            payload (dict): payload with infrastructure configuration
        """
        self.payload = payload

    def get_payload(self):
        """ Getter for payload attribute"""
        return self.payload

    def get_bucketname(self):
        """ Get bucket name """
        if 'BucketName' in self.template:
            return ok(self.template['BucketName'])
        return not_found('Bucket name not found')

    def set_template(self):
        """ Construct Resource for the CloudFormation template from payload """
        for bucket_property in self.payload.keys():
            if bucket_property in self.S3_BUCKET_PROPERTIES:
                self.method_handler(bucket_property)

    def get_template(self):
        """ Method that returns iac template from configuration options """
        return self.template

    @staticmethod
    def construct_tags(tags):
        """ Returns CloudFormation friendly key-value tags

        Args:
            tags (dict): dictionary of key and value tags
        Returns:
            cf_tags (dict): CloudFormation friendly tags
        """
        cf_tags = []
        for key in tags.keys():
            temp = {'Key': key, 'Value': tags[key]}
            cf_tags.append(temp)
        return cf_tags

    def method_handler(self, arg):
        """ Handle all different configurations for an S3 bucket

        Args:
            arg (dict): a payload of the infrastructure to be provisioned
        """
        if arg == "AccelerateConfiguration":
            self.get_acceleration_config(arg)
        if arg == "AccessControl":
            self.get_access_control(arg)
        if arg == "AnalyticsConfiguration":
            self.get_analytics_configuration(arg)
        if arg == "BucketEncryption":
            self.get_bucket_encryption(arg)
        if arg == "BucketName":
            self.get_bucket_name(arg)
        if arg == "CorsConfiguration":
            self.get_cors_configuration(arg)
        if arg == "VersioningConfiguration":
            self.get_version_configuration(arg)
        if arg == "InventoryConfigurations":
            self.get_inventory_configuration(arg)
        if arg == "LifecycleConfiguration":
            self.get_lifecycle_configuration(arg)
        if arg == "LoggingConfiguration":
            self.get_logging_configuration(arg)
        if arg == "MetricsConfigurations":
            self.get_metrics_configuration(arg)
        if arg == "NotificationConfiguration":
            self.get_notification_configuration(arg)
        if arg == "ObjectLockConfiguration":
            self.get_object_lock_configuration(arg)
        if arg == "PublicAccessBlockConfiguration":
            self.get_public_block_configuration(arg)
        if arg == "ReplicationConfiguration":
            self.get_replication_configuration(arg)
        if arg == "Tags":
            self.get_tags(arg)
        if arg == "WebsiteConfiguration":
            self.get_website_configuration(arg)

    def get_acceleration_config(self, arg):
        """ Check to validate acceleration configuration from a given payload

        if payload satisfies validation, acceleration configuration is added to
        self.template

        Args:
            arg (dict): a given payload
        """
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
        """ Check to validate access control configuration from a given payload

        if payload satisfies validation, access control configuration is added to
        self.template

        Args:
            arg (dict): a given payload
        """
        accepted_options = [
            "private", "public-read", "public-read-write",
            "aws-exec-read", "authenticated-read", "bucket-owner-read",
            "bucket-owner-full-control", "log-delivery-write"
        ]
        bucket_property = self.payload[arg]
        if isinstance(bucket_property, str):
            if bucket_property in accepted_options:
                self.template[arg] = bucket_property

    def get_analytics_configuration(self, arg):
        """ Check to validate analytics configuration from a given payload

        if payload satisfies validation, analytics configuration is added to
        self.template

        Args:
            arg (dict): a given payload
        """
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
                        template[prop] = self.construct_tags(bucket_property[prop])
                    else:
                        template[prop] = bucket_property[prop]
        if "StorageClassAnalysis" in template:
            self.template[arg] = template

    def get_bucket_encryption(self, arg):
        """ Check to validate bucket encryption from a given payload

        if payload satisfies validation, analytics configuration is added to
        self.template

        Args:
            arg (dict): a given payload
        """
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
                "ServerSideEncryptionConfiguration": [{
                    "ServerSideEncryptionByDefault": encryption
                }]
            }

    def get_bucket_name(self, arg):
        """ Check to validate bucket name from given payload

        if payload satisfies validation, bucket name is added to
        self.template

        Args:
            arg (dict): a given payload
        """
        bucket_property = self.payload[arg]
        self.template[arg] = bucket_property

    def get_cors_configuration(self, arg):
        """ Check to validate cors configuration from a given payload

        if payload satisfies validation, cors configuration is added to
        self.template

        Args:
            arg (dict): a given payload
        """
        cors_rules = []
        allowed_methods = ['GET', 'PUT', 'HEAD', 'POST', 'DELTE']
        bucket_property = self.payload[arg]
        for configuration in bucket_property:
            cors_rule = {}
            if "AllowedHeaders" in configuration:
                if isinstance(configuration['AllowedHeaders'], list):
                    cors_rule['AllowedHeaders'] = configuration['AllowedHeaders']
            if "AllowedMethods" in configuration:
                methods = []
                for method in configuration['AllowedMethods']:
                    if method in allowed_methods:
                        methods.append(method)
                cors_rule['AllowedMethods'] = methods
            if "AllowedOrigins" in configuration:
                if isinstance(configuration['AllowedOrigins'], list):
                    cors_rule['AllowedOrigins'] = configuration['AllowedOrigins']
            if "ExposedHeaders" in configuration:
                if isinstance(configuration['ExposedHeaders'], list):
                    cors_rule['ExposedHeaders'] = configuration['ExposedHeaders']
            if "Id" in configuration:
                if configuration["Id"] != "":
                    cors_rule['Id'] = configuration['Id']
            if "MaxAge" in configuration:
                if isinstance(configuration['MaxAge'], int):
                    cors_rule['MaxAge'] = configuration['MaxAge']
            if ("AllowedMethods" in cors_rule) and ("AllowedOrigins" in cors_rule):
                cors_rules.append(cors_rule)
        if len(cors_rules) != 0:
            self.template[arg] = {"CorsRules": cors_rules}

    def get_inventory_configuration(self, arg):
        """ Check to validate inventory configuration from a given payload

        if payload satisfies validation, inventory configuration is added to
        self.template

        Args:
            arg (dict): a given payload
        """
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
                    destination['Format'] = "CSV"
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
                if configuration['Enabled'] or not configuration['Enabled']:
                    inventory['Enabled'] = configuration['Enabled']
            if "Id" in configuration:
                inventory['Id'] = configuration['Id']
            if "IncludedObjectVersions" in configuration:
                if configuration['IncludedObjectVersions'] in ['All', 'Current']:
                    inventory['IncludedObjectVersions'] = configuration['IncludedObjectVersions']
            if "ScheduledFrequency" in configuration:
                if configuration['ScheduledFrequency'] in ['Daily', 'Weekly']:
                    inventory['ScheduledFrequency'] = configuration['ScheduledFrequency']
            if {'Enabled', 'Id', 'IncludedObjectVersions', 'ScheduledFrequency'}.issubset(set(inventory.keys())):
                inventory_configurations.append(inventory)
        if len(inventory_configurations) != 0:
            self.template[arg] = inventory_configurations

    @staticmethod
    def has_lifecycle_configuration_set(properties):
        """ Method that checks if a lifecycle property has been set

        Args:
            properties (dict): properties set for a lifecycle configuration

        Returns:
            bool: depending on if a property has been set
        """
        optional_properties = [
            'AbortIncompleteMultipartUpload', 'ExpirationDate', 'ExpirationInDays',
            'NoncurrentVersionExpirationInDays', 'NoncurrentVersionTransitions',
            'Transitions'
        ]
        for prop in properties:
            if prop in optional_properties:
                return True
        return False

    def get_lifecycle_configuration(self, arg):
        """ Check to validate lifecycle configuration from a given payload

        if payload satisfies validation, lifecycle configuration is added to
        self.template

        Args:
            arg (dict): a given payload
        """
        bucket_property = self.payload[arg]
        storage_class = [
            'DEEP_ARCHIVE', 'GLACIER', 'INTELLIGENT_TIERING', 'ONEZONE_IA', 'STANDARD_IA'
        ]
        life_cycles = []
        for configuration in bucket_property:
            lifecycle = {}
            if "AbortIncompleteMultipartUpload" in configuration:
                days = configuration['AbortIncompleteMultipartUpload']
                if isinstance(days, int):
                    lifecycle['AbortIncompleteMultipartUpload'] = {
                        'DaysAfterInitiation': days}
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
                if self.has_lifecycle_configuration_set(lifecycle):
                    life_cycles.append(lifecycle)
        if len(life_cycles) != 0:
            self.template[arg] = {'Rules': life_cycles}

    def get_version_configuration(self, arg):
        """ Check to validate version_configuration from a given payload

        if payload satisfies validation, version_configuration is added to
        self.template

        Args:
            arg (dict): a given payload
        """
        bucket_property = self.payload[arg]
        if bucket_property in ['Enabled', 'Suspended']:
            self.template[arg] = {"Status": bucket_property}

    def get_logging_configuration(self, arg):
        """ Check to validate logging configuration from a given payload

        if payload satisfies validation, logging configuration is added to
        self.template

        Args:
            arg (dict): a given payload
        """
        logging = {}
        bucket_property = self.payload[arg]
        if 'LogFilePrefix' in bucket_property:
            logging['LogFilePrefix'] = bucket_property['LogFilePrefix']
        if 'DestinationBucketName' in bucket_property:
            logging['DestinationBucketName'] = bucket_property['DestinationBucketName']
        if len(logging.keys()) != 0:
            self.template[arg] = logging

    def get_metrics_configuration(self, arg):
        """ Check to validate metric configuration from a given payload

        if payload satisfies validation, metric configuration is added to
        self.template

        Args:
            arg (dict): a given payload
        """
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
    def get_notification(config):
        """ Validate a notification configuration

        Args:
            config (dict): a notification configuration
            
        Returns:
            notifications (dict): Notification configurations
        """
        notifications = []
        for configuration in config:
            notification = {}
            if 'Event' in configuration:
                notification['Event'] = configuration['Event']
            if 'Filter' in configuration:
                filters = []
                for _filter in configuration['Filter']:
                    if 'Name' in _filter and 'Value' in _filter:
                        if _filter['Name'] in ['prefix', 'suffix']:
                            filters.append(
                                {
                                    'Name': _filter['Name'],
                                    'Value': _filter['Value']
                                })
                if len(filters) != 0:
                    notification['Filter'] = {'S3Key': {'Rules': filters}}
            if "Function" in configuration:
                notification['Function'] = configuration['Function']
            if "Queue" in configuration:
                notification['Queue'] = configuration['Queue']
            if "Topic" in configuration:
                notification['Topic'] = configuration['Topic']
            if 'Event' in notification and 'Filter' in notification:
                if 'Function' in notification or 'Queue' in notification or \
                        'Topic' in configuration:
                    notifications.append(notification)
        return notifications

    def get_notification_configuration(self, arg):
        """ Check to validate notification configuration from a given payload

        if payload satisfies validation, notification configuration is added to
        self.template

        Args:
            arg (dict): a given payload
        """
        notification = {}
        bucket_property = self.payload[arg]
        if 'LambdaConfigurations' in bucket_property:
            config = self.get_notification(bucket_property['LambdaConfigurations'])
            if len(config) != 0:
                notification['LambdaConfigurations'] = config
        if 'QueueConfigurations' in bucket_property:
            config = self.get_notification(bucket_property['QueueConfigurations'])
            if len(config) != 0:
                notification['QueueConfigurations'] = config
        if 'TopicConfigurations' in bucket_property:
            config = self.get_notification(bucket_property['TopicConfigurations'])
            if len(config) != 0:
                notification['TopicConfigurations'] = config
        if len(notification.keys()) != 0:
            self.template[arg] = notification

    def get_object_lock_configuration(self, arg):
        """ Check to validate object lock configuration from a given payload

        if payload satisfies validation, object lock configuration is added to
        self.template

        Args:
            arg (dict): a given payload
        """
        object_lock = {}
        mode = ['COMPLIANCE', 'GOVERNANCE']
        bucket_property = self.payload[arg]
        if 'ObjectLockEnabled' in bucket_property:
            if bucket_property['ObjectLockEnabled'] == 'Enabled':
                object_lock['ObjectLockEnabled'] = 'Enabled'
        if "DefaultRetention" in bucket_property:
            retention = {}
            if 'Days' in bucket_property['DefaultRetention']:
                if isinstance(bucket_property['DefaultRetention']['Days'], int):
                    retention['Days'] = bucket_property['DefaultRetention']['Days']
            if 'Mode' in bucket_property['DefaultRetention']:
                if bucket_property['DefaultRetention']['Mode'] in mode:
                    retention['Mode'] = bucket_property['DefaultRetention']['Mode']
            if 'Years' in bucket_property['DefaultRetention']:
                if isinstance(bucket_property['DefaultRetention']['Years'], int):
                    retention['Years'] = bucket_property['DefaultRetention']['Years']
            if len(retention.keys()) != 0:
                object_lock['Rule'] = {'DefaultRetention': retention}
        if len(object_lock.keys()) != 0:
            if 'ObjectLockEnabled' in object_lock:
                self.template['ObjectLockEnabled'] = True
                self.template['ObjectLockConfiguration'] = object_lock

    def get_public_block_configuration(self, arg):
        """ Check to validate public access block configuration from a given payload

        if payload satisfies validation, public access block configuration is added to
        self.template

        Args:
            arg (dict): a given payload
        """
        bucket_property = self.payload[arg]
        public_block = {}
        public_access_block = [
            'BlockPublicAcls', 'BlockPublicPolicy', 'IgnorePublicAcls', 'RestrictPublicBuckets']
        for key in bucket_property.keys():
            if key in public_access_block:
                if isinstance(bucket_property[key], bool):
                    public_block[key] = bucket_property[key]
        if set(public_access_block).issubset(set(public_block.keys())):
            self.template[arg] = public_block

    def get_replication_configuration(self, arg):
        """ Check to validate replication configuration from a given payload

        if payload satisfies validation, replication configuration is added to
        self.template

        Args:
            arg (dict): a given payload
        """
        replication = {}
        rules = []
        storage_class = [
            'DEEP_ARCHIVE', 'GLACIER', 'INTELLIGENT_TIERING', 'ONEZONE_IA', 'STANDARD_IA'
        ]
        bucket_property = self.payload[arg]
        if "Role" in bucket_property:
            replication['Role'] = bucket_property['Role']
        if "Rules" in bucket_property:
            rules = []
            if isinstance(bucket_property['Rules'], list):
                for rep_rule in bucket_property['Rules']:
                    rule = {}
                    if "Destination" in rep_rule:
                        dest = {}
                        dest_config = rep_rule['Destination']
                        if "Owner" in dest_config and "Account" in dest_config:
                            dest['AccessControlTranslation'] = {
                                'Owner': dest_config['Owner']}
                            dest['Account'] = dest_config['Account']
                        if "ReplicaKmsKeyID" in dest_config:
                            dest['EncryptionConfiguration'] = {
                                'ReplicaKmsKeyID': dest_config['ReplicaKmsKeyID']}
                        if "StorageClass" in dest_config:
                            if dest_config['StorageClass'] in storage_class:
                                dest['StorageClass'] = dest_config['StorageClass']
                        if "Bucket" in dest_config:
                            dest['Bucket'] = dest_config['Bucket']
                            rule['Destination'] = dest
                    if "Id" in rep_rule:
                        rule['Id'] = rep_rule['Id']
                    if "Prefix" in rep_rule:
                        rule['Prefix'] = rep_rule['Prefix']
                    else:
                        rule['Prefix'] = ''
                    if "SseKmsEncryptionEnabled" in rep_rule:
                        rule['SourceSelectionCriteria'] = {
                            'SseKmsEncryptionEnabled': {
                                'Status': rep_rule['SseKmsEncryptionEnabled']
                            }}
                    else:
                        rule['SourceSelectionCriteria'] = {
                            'SseKmsEncryptionEnabled': {
                                'Status': 'Disabled'
                            }}
                    if 'Status' in rep_rule:
                        if rep_rule['Status'] in ['Enabled', 'Suspended']:
                            rule['Status'] = rep_rule['Status']
                    if 'Status' in rule and 'Prefix' in rule and 'Destination' in rule:
                        rules.append(rule)
        if "Role" in replication and len(rules) != 0:
            replication['Rules'] = rules
            self.template['ReplicationConfiguration'] = replication

    def get_tags(self, arg):
        """ Check to validate tags from a given payload

        if payload satisfies validation, tags is added to self.template

        Args:
            arg (dict): a given payload
        """
        bucket_property = self.payload[arg]
        tags = self.construct_tags(bucket_property)
        if len(tags) != 0:
            self.template[arg] = tags

    def get_website_configuration(self, arg):
        """ Check to validate website configuration from a given payload

        if payload satisfies validation, website configuration is added to
        self.template

        Args:
            arg (dict): a given payload
        """
        website = {}
        bucket_property = self.payload[arg]
        if "ErrorDocument" in bucket_property:
            website['ErrorDocument'] = bucket_property['ErrorDocument']
        if "IndexDocument" in bucket_property:
            website['IndexDocument'] = bucket_property['IndexDocument']
        if "RedirectAllRequestsTo" in bucket_property:
            redirect = {}
            if "Protocol" in bucket_property["RedirectAllRequestsTo"]:
                if bucket_property["RedirectAllRequestsTo"]["Protocol"] in ['http', 'https']:
                    redirect['Protocol'] = bucket_property["RedirectAllRequestsTo"]["Protocol"]
            if "Hostname" in bucket_property["RedirectAllRequestsTo"]:
                redirect['Hostname'] = bucket_property["RedirectAllRequestsTo"]["Hostname"]
                website["RedirectAllRequestsTo"] = redirect
        if "RoutingRules" in bucket_property:
            rules = []
            for rule in bucket_property['RoutingRules']:
                routing_rule = {}
                if "RedirectRules" in rule:
                    redirect_rule = {}
                    redirect = rule['RedirectRules']
                    if "HostName" in redirect:
                        redirect_rule['HostName'] = redirect['HostName']
                    if "HttpRedirectCode" in redirect:
                        redirect_rule['HttpRedirectCode'] = redirect['HttpRedirectCode']
                    if "Protocol" in redirect:
                        if redirect['Protocol'] in ['http', 'https']:
                            redirect_rule['Protocol'] = redirect['Protocol']
                    if "ReplaceKeyPrefixWith" in redirect:
                        redirect_rule['ReplaceKeyPrefixWith'] = redirect['ReplaceKeyPrefixWith']
                    if "ReplaceKeyWith" in redirect:
                        redirect_rule['ReplaceKeyWith'] = redirect['ReplaceKeyWith']
                    if len(redirect_rule.keys()) != 0:
                        routing_rule['RedirectRules'] = redirect_rule
                if "RoutingRuleCondition" in rule:
                    condition = rule['RoutingRuleCondition']
                    routing_condition = {}
                    if "HttpErrorCodeReturnsEquals" in condition:
                        routing_condition['HttpErrorCodeReturnsEquals'] = condition['HttpErrorCodeReturnsEquals']
                    if "KeyPrefixEquals" in condition:
                        routing_condition['KeyPrefixEquals'] = condition['KeyPrefixEquals']
                    if len(routing_condition.keys()) != 0:
                        routing_rule['RoutingRuleCondition'] = routing_condition
                if "RedirectRules" in routing_rule or "RoutingRuleCondition" in routing_rule:
                    rules.append(routing_rule)
            if len(rules) != 0:
                website['RedirectRules'] = rules
        if len(website.keys()) != 0:
            self.template['WebsiteConfiguration'] = website

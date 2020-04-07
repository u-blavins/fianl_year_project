import pytest
from mock import MagicMock
from mock import patch

from infrastructure_provisioner.cf_s3 import S3_CF


class TestS3_CF:
    """ Test Suite for S3 CloudFormation Utility Class """

    def setup_method(self):
        """ Initialise Test Suite """
        mock_payload = {'test': 'test'}
        self.mock_s3_cf = S3_CF(mock_payload)

    def test_set_get_payload(self):
        """ Test Success: Set and get payload """
        expected_payload = {
            'test': 'test_change'
        }
        self.mock_s3_cf.set_payload(expected_payload)
        sut = self.mock_s3_cf.get_payload()
        assert sut == expected_payload

    def test_construct_tags_returns_cf_tags(self):
        """ Test Success: CloudFormation tags returned correctly """
        test_tags = {'test_key': 'test_value'}
        expected_tags = [{
            'Key': 'test_key',
            'Value': 'test_value'
        }]
        sut = self.mock_s3_cf.construct_tags(test_tags)
        assert sut == expected_tags

    def test_get_acceleration_config_adds_enabled_config(self):
        """ Test Success: Acceleration enabled config set within template """
        test_payload = {"AccelerateConfiguration": "Enabled"}
        expected = {'AccelerateConfiguration': {'AccelerationStatus': 'Enabled'}}
        self.mock_s3_cf.set_payload(test_payload)
        self.mock_s3_cf.set_template()
        sut = self.mock_s3_cf.get_template()
        assert sut == expected

    def test_get_acceleration_config_adds_suspended_config(self):
        """ Test Success: Acceleration enabled config set within template """
        test_payload = {"AccelerateConfiguration": "Suspended"}
        expected = {'AccelerateConfiguration': {'AccelerationStatus': 'Suspended'}}
        self.mock_s3_cf.set_payload(test_payload)
        self.mock_s3_cf.set_template()
        sut = self.mock_s3_cf.get_template()
        assert sut == expected

    def test_get_acceleration_config_does_not_add_to_template_on_fail(self):
        """ Test Failure: Acceleration enabled config not added to template with 
        incorrect configuration
        """
        test_payload = {"AccelerateConfiguration": "Test"}
        expected = {}
        self.mock_s3_cf.set_payload(test_payload)
        self.mock_s3_cf.set_template()
        sut = self.mock_s3_cf.get_template()
        assert sut == expected

    def test_get_access_control_adds_access_control(self):
        """ Test Success: Access control set within template """
        test_payload = {"AccessControl": "private"}
        expected = test_payload
        self.mock_s3_cf.set_payload(test_payload)
        self.mock_s3_cf.set_template()
        sut = self.mock_s3_cf.get_template()
        assert sut == expected

    def test_get_access_control_does_not_add_to_template_on_fail(self):
        """ Test Failure: Access control not added to template with 
        incorrect configuration """
        test_payload = {"AccessControl": "test"}
        expected = {}
        self.mock_s3_cf.set_payload(test_payload)
        self.mock_s3_cf.set_template()
        sut = self.mock_s3_cf.get_template()
        assert sut == expected

    def test_get_analytics_configuration_adds_analytic_config(self):
        """ Test Success: Analytic configuration added to template """
        fake_id = "test_id"
        fake_prefix = "test_prefix"
        fake_tag_filters = {'test_key_1': 'test_value_1'}
        fake_destination = {
            "BucketAccountId": "ACCOUNT_NUM",
            "BucketArn": "BUCKET_ARN",
            "Prefix": fake_prefix
        }
        expected = {'AnalyticsConfiguration': {
            'Id': 'test_id',
            'Prefix': 'test_prefix',
            'StorageClassAnalysis': {
                'DataExport': {
                    'BucketAccountId': 'ACCOUNT_NUM',
                    'BucketArn': 'BUCKET_ARN',
                    'Format': 'CSV',
                    'Prefix': 'test_prefix'
                },
                'OutputSchemaVersion': 'V_1'},
            'TagFilters': [
                {'Key': 'test_key_1','Value': 'test_value_1'}]
            }}

        test_payload = {
            "AnalyticsConfiguration": {
                "Id": fake_id,
                "Prefix": fake_prefix,
                "Destination": fake_destination,
                "TagFilters": fake_tag_filters
            }
        }
        self.mock_s3_cf.set_payload(test_payload)
        self.mock_s3_cf.set_template()
        sut = self.mock_s3_cf.get_template()
        assert sut == expected

    def test_get_analytics_configuration_adds_analytic_config_with_only_destination(self):
        """ Test Success: Analytic configuration added with only destination config """
        fake_destination = {
            "BucketAccountId": "ACCOUNT_NUM",
            "BucketArn": "BUCKET_ARN"
        }
        expected = {'AnalyticsConfiguration': {
            'StorageClassAnalysis': {
                'DataExport': {
                    'BucketAccountId': 'ACCOUNT_NUM',
                    'BucketArn': 'BUCKET_ARN',
                    'Format': 'CSV'},
                'OutputSchemaVersion': 'V_1'}
            }}
        test_payload = {
            "AnalyticsConfiguration": {
                "Destination": fake_destination
            }
        }
        self.mock_s3_cf.set_payload(test_payload)
        self.mock_s3_cf.set_template()
        sut = self.mock_s3_cf.get_template()
        assert sut == expected


    def test_get_analytics_configuration_does_not_add_config_if_bucket_arn_absent(self):
        """ Test Failure: Analytic configuration not added """
        fake_id = "test_id"
        fake_prefix = "test_prefix"
        fake_tag_filters = {'test_key_1': 'test_value_1'}
        fake_destination = {
            "BucketAccountId": "ACCOUNT_NUM",
            "Prefix": fake_prefix
        }
        expected = {}
        test_payload = {
            "AnalyticsConfiguration": {
                "Id": fake_id,
                "Prefix": fake_prefix,
                "Destination": fake_destination,
                "TagFilters": fake_tag_filters
            }
        }
        self.mock_s3_cf.set_payload(test_payload)
        self.mock_s3_cf.set_template()
        sut = self.mock_s3_cf.get_template()
        assert sut == expected

    def test_get_bucket_encryption_with_aes(self):
        """ Test Success: Bucket encryption added to template with AES """
        test_payload = {
            "BucketEncryption": {
                "SSEAlgorithm": "AES256"
            }
        }
        expected = {'BucketEncryption': {'ServerSideEncryptionConfiguration': 
        {'ServerSideEncryptionByDefault': {'SSEAlgorithm': 'AES256'}}}}
        self.mock_s3_cf.set_payload(test_payload)
        self.mock_s3_cf.set_template()
        sut = self.mock_s3_cf.get_template()
        assert sut == expected

    def test_get_bucket_encryption_with_kms(self):
        """ Test Success: Bucket encryption added to template with KMS """
        test_payload = {
            "BucketEncryption": {
                "SSEAlgorithm": "aws:kms",
                "KMSMasterKeyID": "test-key"
            }
        }
        expected = {'BucketEncryption': {'ServerSideEncryptionConfiguration': 
        {'ServerSideEncryptionByDefault': {'KMSMasterKeyID': 'test-key', 
        'SSEAlgorithm': 'aws:kms'}}}}
        self.mock_s3_cf.set_payload(test_payload)
        self.mock_s3_cf.set_template()
        sut = self.mock_s3_cf.get_template()
        assert sut == expected
    
    def test_get_bucket_encryption_with_kms_not_added_if_key_absent(self):
        """ Test Failure: Bucket encryption not added to template without KMS ID """
        test_payload = {"BucketEncryption": {"SSEAlgorithm": "aws:kms"}}
        expected = {}
        self.mock_s3_cf.set_payload(test_payload)
        self.mock_s3_cf.set_template()
        sut = self.mock_s3_cf.get_template()
        assert sut == expected

    def test_get_bucket_encryption_does_not_add_encryption_if_algorithm_incorrect(self):
        """ Test Failure: Bucket encryption not added to template without SSEAlgorithm"""
        test_payload = {"BucketEncryption": {"SSEAlgorithm": "test"}}
        expected = {}
        self.mock_s3_cf.set_payload(test_payload)
        self.mock_s3_cf.set_template()
        sut = self.mock_s3_cf.get_template()
        assert sut == expected

    def test_get_cors_configuration_adds_cors_configuration(self):
        """ Test Success: Cors configuration added to template """
        test_payload = {
            "CorsConfiguration": [{
                "AllowedHeaders": ["test-headers"],
                "AllowedMethods": ["GET", "PUT"],
                "AllowedOrigins": ["test-origins"],
                "ExposedHeaders": ["test-exp-headers"],
                "Id": "test-id",
                "MaxAge": 120
            }]
        }
        expected = {'CorsConfiguration': {'CorsRules': [{'AllowedHeaders': ['test-headers'],
            'AllowedMethods': ['GET', 'PUT'],'AllowedOrigins': ['test-origins'],
            'ExposedHeaders': ['test-exp-headers'],'Id': 'test-id','MaxAge': 120}]}}
        self.mock_s3_cf.set_payload(test_payload)
        self.mock_s3_cf.set_template()
        sut = self.mock_s3_cf.get_template()
        assert sut == expected

    def test_get_cors_configuration_does_not_add_configuration_if_props_absent(self):
        """ Test Failure: Cors configuration not added if AllowedMethods and AllowedOrigins
        absent """
        test_payload = {
            "CorsConfiguration": [{
                "AllowedHeaders": ["test-headers"],
                "ExposedHeaders": ["test-exp-headers"],
                "Id": "test-id",
                "MaxAge": 120
            }]
        }
        expected = {}
        self.mock_s3_cf.set_payload(test_payload)
        self.mock_s3_cf.set_template()
        sut = self.mock_s3_cf.get_template()
        assert sut == expected

    def test_get_inventory_configuration_adds_inventory_configuration(self):
        """ Test Success: Inventory configuration added to template """
        fake_id = "test_id"
        fake_prefix = "test_prefix"
        fake_destination = {
            "BucketAccountId": "ACCOUNT_NUM",
            "BucketArn": "BUCKET_ARN",
            "Prefix": fake_prefix
        }
        test_payload = {
            "InventoryConfigurations": [{
                "Destination": fake_destination,
                "Id": fake_id,
                "Enabled": True,
                "IncludedObjectVersions": "All",
                "OptionalFields": ["Size", "LastModifiedDate"],
                "Prefix": fake_prefix,
                "ScheduledFrequency": "Daily"
            }]
        }
        expected = {'InventoryConfigurations': [{'Destination': {'BucketAccountId': 'ACCOUNT_NUM',
            'BucketArn': 'BUCKET_ARN', 'Format': 'CSV', 'Prefix': 'test_prefix'},
            'Enabled': True,
            'Id': 'test_id',
            'IncludedObjectVersions': 'All',
            'OptionalFields': ['Size', 'LastModifiedDate'],
            'Prefix': 'test_prefix',
            'ScheduledFrequency': 'Daily'}]}
        self.mock_s3_cf.set_payload(test_payload)
        self.mock_s3_cf.set_template()
        sut = self.mock_s3_cf.get_template()
        assert sut == expected

    def test_get_inventory_configuration_does_not_add_config_if_mandatory_keys_absent(self):
        """ Test Failure: """
        fake_prefix = "test_prefix"
        fake_destination = {
            "BucketAccountId": "ACCOUNT_NUM",
            "BucketArn": "BUCKET_ARN",
            "Prefix": fake_prefix
        }
        test_payload = {
            "InventoryConfigurations": [{
                "Destination": fake_destination,
                "OptionalFields": ["Size", "LastModifiedDate"],
                "Prefix": fake_prefix,
            }]
        }
        expected = {}
        self.mock_s3_cf.set_payload(test_payload)
        self.mock_s3_cf.set_template()
        sut = self.mock_s3_cf.get_template()
        assert sut == expected

    def test_has_lifecycle_configuration_set_returns_true_if_config_property_present(self):
        """ Test Success: Returns True if property present """
        fake_properties = {
            "AbortIncompleteMultipartUpload": "test",
            "ExpirationDate": "test"
        }
        sut = self.mock_s3_cf.has_lifecycle_configuration_set(fake_properties)
        assert sut
    
    def test_has_lifecycle_configuration_set_returns_false_if_config_property_absent(self):
        """ Test Failure: Returns False if property absent """
        fake_properties = {
            "test": "test"
        }
        sut = self.mock_s3_cf.has_lifecycle_configuration_set(fake_properties)
        assert not sut
    
    def test_get_lifecycle_configuration_abort_incomplete_multipart_upload(self):
        """ Test Success: Lifecycle configuration added with abort incomplete
        multipart upload property """
        test_payload = {
            "LifecycleConfiguration": [{
                "AbortIncompleteMultipartUpload": 123,
                "Id": "test-id",
                "Prefix": "test-prefix",
                "Status": "Enabled"
            }]
        }
        expected = {
            'LifecycleConfiguration': {
                'Rules': [{
                    'AbortIncompleteMultipartUpload': {
                        'DaysAfterInitiation': 123},
                    'Id': 'test-id',
                    'Prefix': 'test-prefix',
                    'Status': 'Enabled'}]}}
        self.mock_s3_cf.set_payload(test_payload)
        self.mock_s3_cf.set_template()
        sut = self.mock_s3_cf.get_template()
        assert sut == expected

    def test_get_lifecycle_configuration_expiration_date(self):
        """ Test Success: Lifecycle configuration added with expiration date property """
        test_payload = {
            "LifecycleConfiguration": [{
                "ExpirationDate": "1241241212",
                "Id": "test-id",
                "Prefix": "test-prefix",
                "Status": "Enabled"
            }]
        }
        expected = {'LifecycleConfiguration': 
            {'Rules': [{'ExpirationDate': "1241241212", 'Id': 'test-id', 
                'Prefix': 'test-prefix', 'Status': 'Enabled'}]}}
        self.mock_s3_cf.set_payload(test_payload)
        self.mock_s3_cf.set_template()
        sut = self.mock_s3_cf.get_template()
        assert sut == expected

    def test_get_lifecycle_configuration_expiration_in_days(self):
        """ Test Success: Lifecycle configuration added with expiration in days property """
        test_payload = {
            "LifecycleConfiguration": [{
                "ExpirationInDays": 123,
                "Id": "test-id",
                "Prefix": "test-prefix",
                "Status": "Enabled"
            }]
        }
        expected = {'LifecycleConfiguration': 
            {'Rules': [{'ExpirationInDays': 123, 'Id': 'test-id', 
                'Prefix': 'test-prefix', 'Status': 'Enabled'}]}}
        self.mock_s3_cf.set_payload(test_payload)
        self.mock_s3_cf.set_template()
        sut = self.mock_s3_cf.get_template()
        assert sut == expected

    def test_get_lifecycle_configuration_noncurrent_version_expiration_in_days(self):
        """ Test Success: Lifecycle configuration added with noncurrent version expiration in 
        days property """
        test_payload = {
            "LifecycleConfiguration": [{
                "NoncurrentVersionExpirationInDays": 123,
                "Id": "test-id",
                "Prefix": "test-prefix",
                "Status": "Enabled"
            }]
        }
        expected = {'LifecycleConfiguration': 
            {'Rules': [{'NoncurrentVersionExpirationInDays': 123, 'Id': 'test-id', 
                'Prefix': 'test-prefix', 'Status': 'Enabled'}]}}
        self.mock_s3_cf.set_payload(test_payload)
        self.mock_s3_cf.set_template()
        sut = self.mock_s3_cf.get_template()
        assert sut == expected

    def test_get_lifecycle_configuration_adds_noncurrent_version_transitions(self):
        """ Test Success: Lifecycle configuration added with noncurrent version transitions 
        property """
        test_payload = {
            "LifecycleConfiguration": [{
                "NoncurrentVersionTransitions": [{
                    "StorageClass": "DEEP_ARCHIVE",
                    "TransitionInDays": 123
                }],
                "Id": "test-id",
                "Prefix": "test-prefix",
                "Status": "Enabled"
            }]
        }
        expected = {'LifecycleConfiguration': {'Rules': [{'Id': 'test-id',
            'NoncurrentVersionTransitions': [{'StorageClass': 'DEEP_ARCHIVE',
            'TransitionInDays': 123}],
            'Prefix': 'test-prefix',
            'Status': 'Enabled'}]}}
        self.mock_s3_cf.set_payload(test_payload)
        self.mock_s3_cf.set_template()
        sut = self.mock_s3_cf.get_template()
        assert sut == expected

    def test_get_lifecycle_configuration_does_not_add_noncurrent_version_transitions(self):
        """ Test Failure: Lifecycle configuration not added with noncurrent version transitions 
        property not set correctly """
        test_payload = {
            "LifecycleConfiguration": [{
                "NoncurrentVersionTransitions": [{"StorageClass": "DEEP_ARCHIVE"}],
                "Id": "test-id",
                "Prefix": "test-prefix",
                "Status": "Enabled"
            }]
        }
        expected = {}
        self.mock_s3_cf.set_payload(test_payload)
        self.mock_s3_cf.set_template()
        sut = self.mock_s3_cf.get_template()
        assert sut == expected

    def test_get_lifecycle_configuration_add_transitions_with_days(self):
        """ Test Success: Lifecycle configuration added with transitions in days property """
        test_payload = {
            "LifecycleConfiguration": [{
                "Transitions": [{
                        "StorageClass": "DEEP_ARCHIVE",
                        "TransitionInDays": 123 
                    }],
                "Id": "test-id",
                "Prefix": "test-prefix",
                "Status": "Enabled"
            }]
        }
        expected = {'LifecycleConfiguration': {'Rules': [{'Id': 'test-id',
            'Prefix': 'test-prefix',
            'Status': 'Enabled',
            'Transitions': [{'StorageClass': 'DEEP_ARCHIVE',
            'TransitionInDays': 123}]}]}}
        self.mock_s3_cf.set_payload(test_payload)
        self.mock_s3_cf.set_template()
        sut = self.mock_s3_cf.get_template()
        assert sut == expected

    def test_get_lifecycle_configuration_add_transitions_with_date(self):
        """ Test Success: Lifecycle configuration added with transitions date property """
        test_payload = {
            "LifecycleConfiguration": [{
                "Transitions": [{
                        "StorageClass": "DEEP_ARCHIVE",
                        "TransitionDate": "21412415"
                    }],
                "Id": "test-id",
                "Prefix": "test-prefix",
                "Status": "Enabled",
                "TagFilters":{"test-key":"test-value"}
            }]
        }
        expected = {'LifecycleConfiguration': {'Rules': [{'Id': 'test-id', 
        'Prefix': 'test-prefix', 'Status': 'Enabled', 'TagFilters': 
        [{'Key': 'test-key', 'Value': 'test-value'}],
        'Transitions': [{'StorageClass': 'DEEP_ARCHIVE', 
        'TransitionDate': '21412415'}]}]}}
        self.mock_s3_cf.set_payload(test_payload)
        self.mock_s3_cf.set_template()
        sut = self.mock_s3_cf.get_template()
        assert sut == expected

    def test_get_lifecycle_configuration_not_set_if_lifecycle_property_absent(self):
        """ Test Failure: Lifecycle configuration not added without lifecycle 
        property """
        test_payload = {
            "LifecycleConfiguration": [{
                "Id": "test-id",
                "Prefix": "test-prefix",
                "Status": "Enabled",
                "TagFilters":{"test-key":"test-value"}
            }]
        }
        expected = {}
        self.mock_s3_cf.set_payload(test_payload)
        self.mock_s3_cf.set_template()
        sut = self.mock_s3_cf.get_template()
        assert sut == expected

    def test_get_lifecycle_configuration_not_set_if_status_absent(self):
        """ Test Failure: Lifecycle configuration not added without status property """
        test_payload = {
            "LifecycleConfiguration": [{
                "Transitions": [{
                        "StorageClass": "DEEP_ARCHIVE",
                        "TransitionDate": "21412415"
                    }],
                "Id": "test-id",
                "Prefix": "test-prefix",
                "TagFilters":{"test-key":"test-value"}
            }]
        }
        expected = {}
        self.mock_s3_cf.set_payload(test_payload)
        self.mock_s3_cf.set_template()
        sut = self.mock_s3_cf.get_template()
        assert sut == expected

    def test_get_version_configuration_added_to_template(self):
        """ Test Success: Version configuration added to template """
        expected_enabled = {"VersionConfiguration": "Enabled"}
        self.mock_s3_cf.set_payload(expected_enabled)
        self.mock_s3_cf.set_template()
        sut_enabled = self.mock_s3_cf.get_template()
        assert sut_enabled == expected_enabled
        expected_suspended = {"VersionConfiguration": "Suspended"}
        self.mock_s3_cf.set_payload(expected_suspended)
        self.mock_s3_cf.set_template()
        sut_suspended = self.mock_s3_cf.get_template()
        assert sut_suspended == expected_suspended

    def test_get_version_configuration_not_added_to_template(self):
        """ Test Failure: Version configuration not added if incorrect """
        test_payload = {"VersionConfiguration": "test"}
        expected = {}
        self.mock_s3_cf.set_payload(test_payload)
        self.mock_s3_cf.set_template()
        sut = self.mock_s3_cf.get_template()
        assert sut == expected

    def test_get_logging_configuration(self):
        """ Test Success: Logging configuration added to template """
        test_payload = {
            "LoggingConfiguration": {
                "DestinationBucketName": "test-bucket",
                "LogFilePrefix": "test-log-file-prefix"
            }
        }
        expected = {'LoggingConfiguration': {
            'DestinationBucketName': 'test-bucket','LogFilePrefix': 'test-log-file-prefix'}}
        self.mock_s3_cf.set_payload(test_payload)
        self.mock_s3_cf.set_template()
        sut = self.mock_s3_cf.get_template()
        assert sut == expected

    def test_get_metrics_configuration_adds_to_template(self):
        """ Test Success: Metrics confirguarion added to template """
        test_payload = {
            "MetricsConfigurations": [
                {
                    "Id": "MetricsConfigurationId",
                    "Prefix": "test-prefix",
                    "TagFilters": {
                        "test-key": "test-value"
                    }
                }
            ]
        }
        expected = {'MetricsConfigurations': [{'Id': 'MetricsConfigurationId',
            'Prefix': 'test-prefix', 'TagFilters': [{'Key': 'test-key',
            'Value': 'test-value'}]}]}
        self.mock_s3_cf.set_payload(test_payload)
        self.mock_s3_cf.set_template()
        sut = self.mock_s3_cf.get_template()
        assert sut == expected

    def test_get_metrics_configuration_does_not_add_to_template(self):
        """ Test Failure: Metrics confirguarion not added to template if id absent """
        test_payload = {
            "MetricsConfigurations": [
                {
                    "Prefix": "test-prefix",
                    "TagFilters": {
                        "test-key": "test-value"
                    }
                }
            ]
        }
        expected = {}
        self.mock_s3_cf.set_payload(test_payload)
        self.mock_s3_cf.set_template()
        sut = self.mock_s3_cf.get_template()
        assert sut == expected

    def test_get_notification_configuration_adds_lambda_to_template(self):
        """ Test Success: Lambda configuration added to template """
        test_payload = {
            "NotificationConfiguration": {
                "LambdaConfigurations": [{
                    "Event": "test-event-name",
                    "Filter": [
                        {"Name": "prefix", "Value": "test-prefix"},
                        {"Name": "suffix", "Value": "test-suffix"}
                    ],
                    "Function": "test-function"
                }]
            }
        }
        expected = {'NotificationConfiguration': {
            'LambdaConfigurations': [{
                'Event': 'test-event-name', 
                'Filter': {
                    'S3Key': {
                        'Rules': [{
                            'Name': 'prefix','Value': 'test-prefix'}, 
                            {'Name': 'suffix', 'Value': 'test-suffix'}]}}, 
                        'Function': 'test-function'}]}}
        self.mock_s3_cf.set_payload(test_payload)
        self.mock_s3_cf.set_template()
        sut = self.mock_s3_cf.get_template()
        assert sut == expected

    def test_get_notification_configuration_adds_sqs_to_template(self):
        """ Test Success: SQS configuration added to template """
        test_payload = {
            "NotificationConfiguration": {
                "QueueConfigurations": [{
                    "Event": "test-event-name",
                    "Filter": [
                        {"Name": "prefix", "Value": "test-prefix"},
                        {"Name": "suffix", "Value": "test-suffix"}
                    ],
                    "Queue": "test-queue"
                }]
            }
        }
        expected = {'NotificationConfiguration': {
            'QueueConfigurations': [{
                'Event': 'test-event-name',
                'Filter': {'S3Key': {'Rules': [{
                    'Name': 'prefix', 'Value': 'test-prefix'},
                    {'Name': 'suffix', 'Value': 'test-suffix'}]}},
                    'Queue': 'test-queue'}]}}
        self.mock_s3_cf.set_payload(test_payload)
        self.mock_s3_cf.set_template()
        sut = self.mock_s3_cf.get_template()
        assert sut == expected

    def test_get_notification_configuration_adds_sns_to_template(self):
        """ Test Success: SNS configuration added to template """
        test_payload = {
            "NotificationConfiguration": {
                "TopicConfigurations": [{
                    "Event": "test-event-name",
                    "Filter": [
                        {"Name": "prefix", "Value": "test-prefix"},
                        {"Name": "suffix", "Value": "test-suffix"}
                    ],
                    "Topic": "test-topic"
                }]
            }
        }
        expected = {'NotificationConfiguration': {
            'TopicConfigurations': [{
                'Event': 'test-event-name',
                'Filter': {'S3Key': {'Rules': [{
                    'Name': 'prefix', 'Value': 'test-prefix'},
                    {'Name': 'suffix', 'Value': 'test-suffix'}]}},
                    'Topic': 'test-topic'}]}}
        self.mock_s3_cf.set_payload(test_payload)
        self.mock_s3_cf.set_template()
        sut = self.mock_s3_cf.get_template()
        assert sut == expected

    def test_get_object_lock_configuration_adds_to_template_without_retention(self):
        """ Test Success: Object lock configuration added to template without retention """
        test_payload = {
            "ObjectLockConfiguration": {"ObjectLockEnabled": "Enabled"}
        }
        expected = {'ObjectLockConfiguration': {'ObjectLockEnabled': 'Enabled'},
            'ObjectLockEnabled': True}
        self.mock_s3_cf.set_payload(test_payload)
        self.mock_s3_cf.set_template()
        sut = self.mock_s3_cf.get_template()
        assert sut == expected

    def test_get_object_lock_configuration_adds_to_template_with_retention(self):
        """ Test Success: Object lock configuration added to template with retention """
        test_payload = {
            "ObjectLockConfiguration": {
                "ObjectLockEnabled": "Enabled",
                "DefaultRetention": {
                    "Days": 123,
                    "Mode": "GOVERNANCE",
                    "Years": 1
                }
            }
        }
        expected = {
            'ObjectLockEnabled': True,
            'ObjectLockConfiguration': {
            'ObjectLockEnabled': 'Enabled',
            'Rule': {'DefaultRetention': {'Days': 123, 'Mode': 'GOVERNANCE', 'Years': 1}}}}
        self.mock_s3_cf.set_payload(test_payload)
        self.mock_s3_cf.set_template()
        sut = self.mock_s3_cf.get_template()
        assert sut == expected
    
    def test_get_object_lock_configuration_does_not_add_to_template_not_enabled(self):
        """ Test Failure: Object lock configuration not added to template if not enabled """
        test_payload = {
            "ObjectLockConfiguration": {"DefaultRetention": {
                    "Days": 123,
                    "Mode": "GOVERNANCE",
                    "Years": 1
                }}
        }
        expected = {}
        self.mock_s3_cf.set_payload(test_payload)
        self.mock_s3_cf.set_template()
        sut = self.mock_s3_cf.get_template()
        assert sut == expected

    def test_get_public_block_configuration_adds_to_template(self):
        """ Test Success: Public block configuration added to template """
        test_payload = {
            "PublicAccessBlockConfiguration": {
                "BlockPublicAcls": True,
                "BlockPublicPolicy": True,
                "IgnorePublicAcls": False,
                "RestrictPublicBuckets": True
            }
        }
        expected = {'PublicAccessBlockConfiguration': {
            'BlockPublicAcls': True,
            'BlockPublicPolicy': True,
            'IgnorePublicAcls': False,
            'RestrictPublicBuckets': True}}
        self.mock_s3_cf.set_payload(test_payload)
        self.mock_s3_cf.set_template()
        sut = self.mock_s3_cf.get_template()
        assert sut == expected

    def test_get_replication_configuration_adds_to_template(self):
        """ Test Success: Replication configuration added to template """
        test_payload = {
            "ReplicationConfiguration": {
                "Role": "test-role",
                "Rules": [{
                    "Destination": {
                        "Owner": "test-owner",
                        "Account": "test-account",
                        "Bucket": "test-bucket",
                        "ReplicaKmsKeyID": "test-key-id",
                        "StorageClass": "DEEP_ARCHIVE"
                    },
                    "Id": "test-id",
                    "Prefix": "test-prefix",
                    "SseKmsEncryptionEnabled": "Disabled",
                    "Status": "Enabled"
                }]
            }
        }
        expected = {'ReplicationConfiguration': {
            'Role': 'test-role',
            'Rules': [{
                'Destination': {
                    'AccessControlTranslation': {
                        'Owner': 'test-owner'
                    },
                    'Account': 'test-account',
                    'EncryptionConfiguration': {
                        'ReplicaKmsKeyID': 'test-key-id'
                    },
                    'Bucket': 'test-bucket',
                    'StorageClass': 'DEEP_ARCHIVE'
                },
                'Id': 'test-id',
                'Prefix': 'test-prefix',
                'SourceSelectionCriteria': {'SseKmsEncryptionEnabled': {'Status': 'Disabled'}},
                'Status': 'Enabled'}]}}
        self.mock_s3_cf.set_payload(test_payload)
        self.mock_s3_cf.set_template()
        sut = self.mock_s3_cf.get_template()
        assert sut == expected

    def test_get_replication_configuration_adds_to_template_without_sse(self):
        """ Test Success: Replication configuration added to template without sse """
        test_payload = {
            "ReplicationConfiguration": {
                "Role": "test-role",
                "Rules": [{
                    "Destination": {
                        "Bucket": "test-bucket",
                    },
                    "Id": "test-id",
                    "Status": "Enabled"
                }]
            }
        }
        expected = {'ReplicationConfiguration': {
            'Role': 'test-role',
            'Rules': [{
                'Destination': {'Bucket': 'test-bucket'},
                'Id': 'test-id', 'Prefix': '', 'SourceSelectionCriteria': {
                    'SseKmsEncryptionEnabled': {'Status': 'Disabled'}},
                    'Status': 'Enabled'}]}}
        self.mock_s3_cf.set_payload(test_payload)
        self.mock_s3_cf.set_template()
        sut = self.mock_s3_cf.get_template()
        assert sut == expected

    def test_get_replication_configuration_does_not_add_to_template_without_role(self):
        """ Test Success: Replication configuration not added to template if incorrect
        without role """
        test_payload = {
            "ReplicationConfiguration": {
                "Rules": [{
                    "Destination": {
                        "Bucket": "test-bucket",
                    },
                    "Id": "test-id",
                    "Status": "Enabled"
                }]
            }
        }
        expected = {}
        self.mock_s3_cf.set_payload(test_payload)
        self.mock_s3_cf.set_template()
        sut = self.mock_s3_cf.get_template()
        assert sut == expected

    def test_get_replication_configuration_does_not_add_to_template_without_props(self):
        """ Test Success: Replication configuration not added to template if incorrect
        without other properties """
        test_payload = {
            "ReplicationConfiguration": {
                "Role": "test-role",
                "Rules": [{
                    "Destination": {
                        'Account': 'test-account'
                    },
                    "Id": "test-id"
                }]
            }
        }
        expected = {}
        self.mock_s3_cf.set_payload(test_payload)
        self.mock_s3_cf.set_template()
        sut = self.mock_s3_cf.get_template()
        assert sut == expected

    def test_get_tags_returns_tags_and_adds_to_template(self):
        """ Test Success: CloudFormation tags returned correctly and added
        to template """
        test_payload = {
            "Tags": {
                "test-key": "test-value"
            }
        }
        expected = {'Tags': [{'Key': 'test-key', 'Value': 'test-value'}]}
        self.mock_s3_cf.set_payload(test_payload)
        self.mock_s3_cf.set_template()
        sut = self.mock_s3_cf.get_template()
        assert sut == expected

    def test_get_website_configuration_adds_to_template(self):
        """ Test Success: Website configuration added to template """
        test_payload = {
            "WebsiteConfiguration": {
                "ErrorDocument": "test-error",
                "IndexDocument": "test-index",
                "RedirectAllRequestsTo": {
                    "Hostname": "test-host",
                    "Protocol": "http"
                },
                "RoutingRules": [{
                    "RedirectRules": {
                        "HostName": "test-host",
                        "HttpRedirectCode": "test-redirect-code",
                        "Protocol": "http",
                        "ReplaceKeyPrefixWith": "test-prefix",
                        "ReplaceKeyWith": "test-prefix"
                    },
                    "RoutingRuleCondition": {
                        "HttpErrorCodeReturnsEquals": "test-error-code",
                        "KeyPrefixEquals": "test-prefix"
                    }
                }]
            }
        }
        expected = {'WebsiteConfiguration': {
            'ErrorDocument': 'test-error',
            'IndexDocument': 'test-index',
            'RedirectAllRequestsTo': {
                'Hostname': 'test-host', 'Protocol': 'http'},
                'RedirectRules': [{'RedirectRules': {'HostName': 'test-host',
                'HttpRedirectCode': 'test-redirect-code','Protocol': 'http',
                'ReplaceKeyPrefixWith': 'test-prefix', 'ReplaceKeyWith': 'test-prefix'},
                'RoutingRuleCondition': {'HttpErrorCodeReturnsEquals': 'test-error-code',
                'KeyPrefixEquals': 'test-prefix'}}]}}
        self.mock_s3_cf.set_payload(test_payload)
        self.mock_s3_cf.set_template()
        sut = self.mock_s3_cf.get_template()
        assert sut == expected
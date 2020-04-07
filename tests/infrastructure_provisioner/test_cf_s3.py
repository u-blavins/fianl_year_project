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
            "Destination": fake_destination,
            "Id": fake_id,
            "Enabled": True,
            "IncludedObjectVersions": "All",
            "OptionalFields": ["Size", "LastModifiedDate"],
            "Prefix": fake_prefix,
            "ScheduledFrequency": "Daily"
        }
        expected = {}
        self.mock_s3_cf.set_payload(test_payload)
        self.mock_s3_cf.set_template()
        sut = self.mock_s3_cf.get_template()
        assert sut == expected
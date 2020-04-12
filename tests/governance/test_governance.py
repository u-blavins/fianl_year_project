import pytest
from mock import MagicMock, patch
from copy import deepcopy

from governance.governance import Governance as Gov
from governance.governance import S3_Governance as S3_Gov


class TestGovernance:
    """ Test Suite for the Governance Class """

    def setup_method(self):
        """ Initialise Test Suite """
        self.mock_template = {
            'Resources': {'Bucket': {
                'Type': 'AWS::S3::Bucket',
                'Properties': {'BucketName': 'test-bucket-name'}}
            }}
        self.mock_governance = Gov()

    def test_template_empty_if_not_set(self):
        """ Test Success: Template is empty if not set """
        sut = self.mock_governance.get_template()
        assert sut == {}

    def test_resources_empty_if_not_set(self):
        """ Test Success: Resources is empty if not set """
        test_template = {}
        expected = {}
        self.mock_governance.set_template(template=test_template)
        sut = self.mock_governance.get_resources()
        assert sut == expected

    def test_resources_empty_if_type_not_valid(self):
        """ Test Failure: Resources is empty if type is not valid """
        test_template = {
            'Resources': {'Bucket': {
                'Type': 'AWS::IAM::Role',
                'Properties': {'RoleName': 'test-iam-role'}
            }}
        }
        expected = {}
        self.mock_governance.set_template(template=test_template)
        sut = self.mock_governance.get_resources()
        assert sut == expected

    def test_set_get_template(self):
        """ Test Success: Set and get template """
        self.mock_governance.set_template(template=self.mock_template)
        sut = self.mock_governance.get_template()
        assert sut == self.mock_template

    def test_set_get_template_sets_resources(self):
        """ Test Success: Setting template sets resources correctly """
        expected_resources = {'AWS::S3::Bucket': {'BucketName': 'test-bucket-name'}}
        self.mock_governance.set_template(template=self.mock_template)
        sut = self.mock_governance.get_resources()
        assert sut == expected_resources

    def test_validate_does_not_change_template_with_invalid_type(self):
        """ Test Failure: Validate does not change original template if 
        type is invalid  
        """
        expected_template = {
            'Resources': {'Bucket': {
                'Type': 'AWS::IAM::Role',
                'Properties': {'RoleName': 'test-iam-role'}
            }}
        }
        self.mock_governance.set_template(template=expected_template)
        self.mock_governance.validate()
        sut = self.mock_governance.get_template()
        assert sut == expected_template

    def test_validate_does_change_template_with_valid_type(self):
        """ Test Success: Validate changes original template if type valid """
        expected_template = {
            'Resources': {'Bucket': {
                'Type': 'AWS::S3::Bucket',
                'Properties': {'BucketName': 'test-bucket-name'}}
            }}
        self.mock_governance.set_template(template=self.mock_template)
        self.mock_governance.get_resources()
        self.mock_governance.validate()
        sut = self.mock_governance.get_template()
        assert sut != expected_template


class TestS3_Gov:
    """ Test Suite for the S3 Governance Class """

    def setup_method(self):
        """ Initialise Test Suite """
        self.mock_template = {
            'Resources': {'Bucket': {
                'Type': 'AWS::S3::Bucket',
                'Properties': {'BucketName': 'test-bucket-name'}}
            }}
        self.mock_governance = Gov()

    def test_read_governance_rules(self):
        """ Test Success: Rules are set from file """
        expected_type = 'AWS::S3::Bucket'
        self.mock_governance.set_template(template=self.mock_template)
        self.mock_governance.get_resources()
        resources = self.mock_governance.get_resources()
        mock_s3_gov = S3_Gov(res_type=expected_type,
            res_property=resources[expected_type])
        rules = mock_s3_gov.get_rules()
        assert 'BucketEncryption' in rules
        assert 'VersioningConfiguration' in rules
        assert 'PublicAccessBlockConfiguration' in rules
        assert 'AccessControl' in rules

    def test_bucket_encryption_validates_no_encryption(self):
        """ Test Success: Validates no encryption and sets mandatory encryption """
        test_template = deepcopy(self.mock_template)
        expected_mandatory = {
            'ServerSideEncryptionConfiguration': [{
                    'ServerSideEncryptionByDefault': {
                        'SSEAlgorithm': 'AES256'
                    }}]
        }
        self.mock_governance.set_template(template=test_template)
        self.mock_governance.get_resources()
        self.mock_governance.validate()
        sut = test_template['Resources']['Bucket']['Properties']['BucketEncryption']
        assert sut == expected_mandatory
        assert test_template != self.mock_template


    def test_bucket_encryption_validates_incorrect_encryption(self):
        """ Test Success: Validates incorrect encryption and sets mandatory encryption """
        test_template = deepcopy(self.mock_template)
        properties = test_template['Resources']['Bucket']['Properties']
        properties['BucketEncryption'] = {
            'ServerSideEncryptionConfiguration': [{
                    'ServerSideEncryptionByDefault': {
                        'Test': 'test'
                    }}]
        }
        expected_mandatory = {
            'ServerSideEncryptionConfiguration': [{
                    'ServerSideEncryptionByDefault': {
                        'SSEAlgorithm': 'AES256'
                    }}]
        }
        self.mock_governance.set_template(template=test_template)
        self.mock_governance.get_resources()
        self.mock_governance.validate()
        sut = test_template['Resources']['Bucket']['Properties']['BucketEncryption']
        assert sut == expected_mandatory


    def test_bucket_encryption_validates_bucket_encryption_mandatory(self):
        """ Test Success: Validates mandatory encryption """
        test_template = deepcopy(self.mock_template)
        properties = test_template['Resources']['Bucket']['Properties']
        properties['BucketEncryption'] = {
            'ServerSideEncryptionConfiguration': [{
                    'ServerSideEncryptionByDefault': {
                        'SSEAlgorithm': 'AES256'
                    }}]
        }
        expected_mandatory = {
            'ServerSideEncryptionConfiguration': [{
                    'ServerSideEncryptionByDefault': {
                        'SSEAlgorithm': 'AES256'
                    }}]
        }
        self.mock_governance.set_template(template=test_template)
        self.mock_governance.get_resources()
        self.mock_governance.validate()
        sut = test_template['Resources']['Bucket']['Properties']['BucketEncryption']
        assert sut == expected_mandatory

    def test_bucket_encryption_validates_bucket_encrpytion_accepted(self):
        """ Test Success: Validates accepted encryption """
        test_template = deepcopy(self.mock_template)
        properties = test_template['Resources']['Bucket']['Properties']
        properties['BucketEncryption'] = {
            'ServerSideEncryptionConfiguration': [{
                    'ServerSideEncryptionByDefault': {
                        'SSEAlgorithm': 'aws:kms',
                        'KMSMasterKeyID': '13056591-9cca-457d-84d0-d262c4c370f0'
                    }}]
        }
        expected_accepted = {
            'ServerSideEncryptionConfiguration': [{
                    'ServerSideEncryptionByDefault': {
                        'SSEAlgorithm': 'aws:kms',
                        'KMSMasterKeyID': '13056591-9cca-457d-84d0-d262c4c370f0'
                    }}]
        }
        self.mock_governance.set_template(template=test_template)
        self.mock_governance.get_resources()
        self.mock_governance.validate()
        sut = test_template['Resources']['Bucket']['Properties']['BucketEncryption']
        assert sut == expected_accepted

    def test_version_configuration_validates_no_versioning(self):
        """ Test Success: Validates no versioning and sets mandatory """
        test_template = deepcopy(self.mock_template)
        expected_mandatory = {'Status': 'Enabled'}
        self.mock_governance.set_template(template=test_template)
        self.mock_governance.get_resources()
        self.mock_governance.validate()
        sut = test_template['Resources']['Bucket']['Properties']['VersioningConfiguration']
        assert sut == expected_mandatory
        assert test_template != self.mock_template

    def test_version_configuration_validates_diasabled_versioning(self):
        """ Test Success: Validates disabled versioning and sets mandatory """
        test_template = deepcopy(self.mock_template)
        properties = test_template['Resources']['Bucket']['Properties']
        properties['VersioningConfiguration'] = {'Status': 'Suspended'}
        expected_mandatory = {'Status': 'Enabled'}
        self.mock_governance.set_template(template=test_template)
        self.mock_governance.get_resources()
        self.mock_governance.validate()
        sut = test_template['Resources']['Bucket']['Properties']['VersioningConfiguration']
        assert sut == expected_mandatory

    def test_version_configuration_validates_enabled_versioning(self):
        """ Test Success: Validates enabled versioning and sets mandatory """
        test_template = deepcopy(self.mock_template)
        properties = test_template['Resources']['Bucket']['Properties']
        properties['VersioningConfiguration'] = {'Status': 'Enabled'}
        expected_mandatory = {'Status': 'Enabled'}
        self.mock_governance.set_template(template=test_template)
        self.mock_governance.get_resources()
        self.mock_governance.validate()
        sut = test_template['Resources']['Bucket']['Properties']['VersioningConfiguration']
        assert sut == expected_mandatory

    def test_public_access_validates_no_public_access_config(self):
        """ Test Success: Validates no public access config and sets mandatory public access """
        test_template = deepcopy(self.mock_template)
        expected_mandatory = {
            'BlockPublicAcls': True,
            'BlockPublicPolicy': True,
            'IgnorePublicAcls': True,
            'RestrictPublicBuckets': True
        }
        self.mock_governance.set_template(template=test_template)
        self.mock_governance.get_resources()
        self.mock_governance.validate()
        sut = test_template['Resources']['Bucket']['Properties']['PublicAccessBlockConfiguration']
        assert sut == expected_mandatory
        assert test_template != self.mock_template
    
    def test_public_access_validates_incorrect_public_access_config(self):
        """ 
        Test Success: Validates incorrect public access config and sets mandatory public access 
        """
        test_template = deepcopy(self.mock_template)
        properties = test_template['Resources']['Bucket']['Properties']
        properties['PublicAccessBlockConfiguration'] = {'Test':'test'}
        expected_mandatory = {
            'BlockPublicAcls': True,
            'BlockPublicPolicy': True,
            'IgnorePublicAcls': True,
            'RestrictPublicBuckets': True
        }
        self.mock_governance.set_template(template=test_template)
        self.mock_governance.get_resources()
        self.mock_governance.validate()
        sut = test_template['Resources']['Bucket']['Properties']['PublicAccessBlockConfiguration']
        assert sut == expected_mandatory
    
    def test_public_access_validates_mandatory_public_access_config(self):
        """ Test Success: Validates mandatory public access config """
        test_template = deepcopy(self.mock_template)
        properties = test_template['Resources']['Bucket']['Properties']
        properties['PublicAccessBlockConfiguration'] = {
            'BlockPublicAcls': True,
            'BlockPublicPolicy': True,
            'IgnorePublicAcls': True,
            'RestrictPublicBuckets': True
        }
        expected_mandatory = {
            'BlockPublicAcls': True,
            'BlockPublicPolicy': True,
            'IgnorePublicAcls': True,
            'RestrictPublicBuckets': True
        }
        self.mock_governance.set_template(template=test_template)
        self.mock_governance.get_resources()
        self.mock_governance.validate()
        sut = test_template['Resources']['Bucket']['Properties']['PublicAccessBlockConfiguration']
        assert sut == expected_mandatory

    def test_public_access_validates_accepted_public_access_config(self):
        """ Test Success: Validates accepted public access config """
        test_template = deepcopy(self.mock_template)
        properties = test_template['Resources']['Bucket']['Properties']
        properties['PublicAccessBlockConfiguration'] = {
            'BlockPublicAcls': True,
            'BlockPublicPolicy': False,
            'IgnorePublicAcls': True,
            'RestrictPublicBuckets': False
        }
        expected_accepted = {
            'BlockPublicAcls': True,
            'BlockPublicPolicy': False,
            'IgnorePublicAcls': True,
            'RestrictPublicBuckets': False
        }
        self.mock_governance.set_template(template=test_template)
        self.mock_governance.get_resources()
        self.mock_governance.validate()
        sut = test_template['Resources']['Bucket']['Properties']['PublicAccessBlockConfiguration']
        assert sut == expected_accepted

    def test_access_control_validates_no_access_control(self):
        """ Test Success: Validates no access control and sets mandatory """
        test_template = deepcopy(self.mock_template)
        expected_mandatory = 'bucket-owner-full-control'
        self.mock_governance.set_template(template=test_template)
        self.mock_governance.get_resources()
        self.mock_governance.validate()
        sut = test_template['Resources']['Bucket']['Properties']['AccessControl']
        assert sut == expected_mandatory
        assert test_template != self.mock_template

    def test_access_control_validates_incorrect_access_control(self):
        """ Test Success: Validates incorrect access control and sets mandatory """
        test_template = deepcopy(self.mock_template)
        properties = test_template['Resources']['Bucket']['Properties']
        properties['AccessControl'] = 'test'
        expected_mandatory = 'bucket-owner-full-control'
        self.mock_governance.set_template(template=test_template)
        self.mock_governance.get_resources()
        self.mock_governance.validate()
        sut = test_template['Resources']['Bucket']['Properties']['AccessControl']
        assert sut == expected_mandatory

    def test_access_control_validates_mandatory_access_control(self):
        """ Test Success: Validates mandatory access control """
        test_template = deepcopy(self.mock_template)
        properties = test_template['Resources']['Bucket']['Properties']
        properties['AccessControl'] = 'bucket-owner-full-control'
        expected_mandatory = 'bucket-owner-full-control'
        self.mock_governance.set_template(template=test_template)
        self.mock_governance.get_resources()
        self.mock_governance.validate()
        sut = test_template['Resources']['Bucket']['Properties']['AccessControl']
        assert sut == expected_mandatory

    def test_access_control_validates_accepted_access_control(self):
        """ Test Success: Validates accepted access control """
        test_template = deepcopy(self.mock_template)
        properties = test_template['Resources']['Bucket']['Properties']
        properties['AccessControl'] = 'private'
        expected_accepted = 'private'
        self.mock_governance.set_template(template=test_template)
        self.mock_governance.get_resources()
        self.mock_governance.validate()
        sut = test_template['Resources']['Bucket']['Properties']['AccessControl']
        assert sut == expected_accepted
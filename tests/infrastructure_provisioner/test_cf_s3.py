import pytest
from mock import MagicMock
from mock import patch

from infrastructure_provisioner.cf_s3 import S3_CF


class TestS3CF:
    """ Test Suite fir S3 CloudFormation Utility Class """

    # def test_construct_tags(self):
    #     """ Test Success: Correct set of CF tags returned """
    #     fake_tags = [ {"Info": "Test value"},
    #         {"Owner": "test@test.com"},{"Team": "test"}]
    #     expected_outcome = [
    #         {"Key": "Info", "Value": "Test value"},
    #         {"Key": "Owner", "Value": "test@test.com"},
    #         {"Key": "Team", "Value": "test"} ]
    #     payload = MagicMock()
    #     sut = S3_CF(payload).construct_tags(fake_tags)
    #     assert(sut == expected_outcome)
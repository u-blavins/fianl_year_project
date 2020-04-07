import pytest
from utils.response import *


class TestResponse:
    """ Test Suite for the Response Functions """

    @staticmethod
    def test_ok_response():
        """ Test Success: OK Response message created """
        test_message = "test message"
        expected_result = {
            "ResponseCode": 200,
            "Message": test_message
        }
        sut = ok("test message")
        assert sut == expected_result

    @staticmethod
    def test_created_response():
        """ Test Success: CREATED Response message created """
        test_message = "test message"
        expected_result = {
            "ResponseCode": 201,
            "Message": test_message
        }
        sut = created("test message")
        assert sut == expected_result

    @staticmethod
    def test_bad_request_response():
        """ Test Success: BAD REQUEST Response message created """
        test_message = "test message"
        expected_result = {
            "ResponseCode": 400,
            "Message": test_message
        }
        sut = bad_request("test message")
        assert sut == expected_result

    @staticmethod
    def test_unauthorised_response():
        """ Test Success: UNAUTHORISED Response message created """
        test_message = "test message"
        expected_result = {
            "ResponseCode": 401,
            "Message": test_message
        }
        sut = unauthorised("test message")
        assert sut == expected_result

    @staticmethod
    def test_not_found_response():
        """ Test Success: NOT FOUND Response message created """
        test_message = "test message"
        expected_result = {
            "ResponseCode": 404,
            "Message": test_message
        }
        sut = not_found("test message")
        assert sut == expected_result

    @staticmethod
    def test_conflict_response():
        """ Test Success: CONFLICT Response message created """
        test_message = "test message"
        expected_result = {
            "ResponseCode": 409,
            "Message": test_message
        }
        sut = conflict("test message")
        assert sut == expected_result

    @staticmethod
    def test_internal_server_error_response():
        """ Test Success: INTERNAL SERVER ERROR Response message created """
        test_message = "test message"
        expected_result = {
            "ResponseCode": 500,
            "Message": test_message
        }
        sut = internal_server_error("test message")
        assert sut == expected_result

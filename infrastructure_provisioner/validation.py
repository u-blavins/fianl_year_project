import json
import yaml

class Validation:
    """Class for validating that service is compliant before deployment"""

    def __init__(self, payload):
        """ Initialise class """
        self.payload = payload

    def get_service(self):
        """ Return the service type """
        if isinstance(self.payload, list):
            
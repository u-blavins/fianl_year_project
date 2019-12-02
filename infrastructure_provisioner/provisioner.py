import yaml
import json


class ServiceProvisioner:
    """Class for provisioning infrastructure request by user"""

    def __init__(self, service, payload):
        self.service = service
        self.stack = payload
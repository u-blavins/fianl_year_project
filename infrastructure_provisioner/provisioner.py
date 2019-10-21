import yaml


class ServiceProvisioner:
    """Class for provisioning infrastructure request by user"""

    def __init__(self, service, payload):
        self.service = service
        self.payload = payload

    

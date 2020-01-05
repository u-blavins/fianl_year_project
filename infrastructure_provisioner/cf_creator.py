import yaml
import json

class IAC_CREATOR:
    """Class for creating CloudFormation templates for a service"""

    def __init__(self, payload):
        """Initialise class"""
        self.payload = payload
        self.iac_template = {}
        self.service = self.get_services()
    
    def get_services(self):
        """Method that retrieves services to"""

    def return_template(self):
        return self.iac_template


def get_payload(file_path):
    """ Function that retrieves payload from a file"""
    with open(file_path) as file:
        payload = yaml.safe_load(file)
    return payload

def main():
    payload = get_payload("../iac_templates/payload.yaml")
    return 0

if __name__ == '__main__':
    main()
import boto3


class Client:
    """ Class for creating an AWS boto3 client

    Args:
        service (str): Name of the service to use
        account (str): AWS account number
        role (str): Role name to use
        region (str): Region name that is in use
    
    Attributes:
        service (str): Store the name of the service of use
        account (str): Store the account number
        role (str): Store the name of the role used by account number
        region (str): Store the name of the region
        
    """

    def __init__(self, service, account, role, region):
        """ Instantiate Client Object """
        self.service = service
        self.account = account
        self.role = role
        self.region = region

    def __get_assume_role_session(self, **args):
        """ Assume into an iam role and return a boto3 session

        Args:
            **args: RoleArn (str) and RoleSessionName (str) are required
            for creating a boto3 session 

        Returns:

        """
        sts_client = boto3.client('sts')
        try:
            client = sts_client.assume_role(**args)
            credentials = client['Credentials']

            return {
                'AccessKeyId': credentials['AccessKeyId'],
                'SecretAccessKeyId': credentials['SecretAccessKeyId'],
                'SessionToken': credentials['SessionToken']
            }
        except Exception as e:
            print("Exception: {}".format(e))

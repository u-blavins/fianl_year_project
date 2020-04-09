import json
from utils.response import ok
from utils.response import bad_request


def audit_handler(event, context):
    """ Lambda handler to handle audit of the deployment
    of CloudFormation Templates

    Args:
        event (dict): event details from request
        context (dict): context of the lambda function

    Returns:
        response (dict): response built from handler
    """

    env = event['Environment']
    template = event['Template']
    upload = backup_cft(env=env, template=template)
    email = email_account_owner(template=template)

    response = {}
    response['Test'] = 'Audit Lambda Handler'
    response['Env'] = env
    response['Template'] = template
    response['Upload'] = upload
    response['Email'] = email

    return response

def backup_cft(env, template):
    """ Function that performs a backup of a CloudFormation 
    template to S3

    Args:
        env (dict): environment variables
        template (dict): CloudFormation template
    
    Returns:
        response (dict): response to performing backup
    """
    return ok("mimic what backup would do")

def email_account_owner(template):
    """ Function that sends a notification to account owner 
    notifying that infrastructure has been deployed

    Args:
        env (dict): environment variables
        template (dict): CloudFormation template
    
    Returns:
        response (dict): response to performing backup
    """
    return ok("mimic what email would do")
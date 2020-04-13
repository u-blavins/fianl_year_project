import json

from utils.response import ok
from utils.response import bad_request
from aws_utils.s3 import S3
from aws_utils.ses import SES

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
    backup_bucket = S3()
    try:
        resp = backup_bucket.backup_cloudformation_temlates(
        template=template)

        status = resp['ResponseMetaData']['HTTPStatusCode']

        if status == 200:
            response = ok("Bucket successfully backed up to S3")
        if status == 400:
            response = bad_request("Not able to back up to S3")

    except:
        response = bad_request('Issue connecting to S3')

    return response

def email_account_owner(template):
    """ Function that sends a notification to account owner 
    notifying that infrastructure has been deployed

    Args:
        env (dict): environment variables
        template (dict): CloudFormation template
    
    Returns:
        response (dict): response to performing backup
    """
    ses = SES()

    try: 
        resp = ses.upload_cft_deploy_email(template=template)

        status = resp['ResponseMetaData']['HTTPStatusCode']

        if status == 200:
            response = ok("Email sent to account owner")
        if status == 400:
            response = bad_request("Email not sent")

    except:
        response = bad_request("Issue with connecting to SES")
    
    return response
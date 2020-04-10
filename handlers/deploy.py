import json
import boto3

from infrastructure_provisioner.cf_builder import CF_BUILDER
from infrastructure_provisioner.cf_s3 import S3_CF
from utils.response import ok
from utils.response import bad_request

def deploy_governed_template_handler(event, context):
    """ Lambda handler to handles the deployment
    of governed CloudFormation Templates

    Args:
        event (dict): event details from request
        context (dict): context of the lambda function

    Returns:
        response (dict): response built from handler
    """

    template = event['Template']

    response = {}
    response['Test'] = 'Deploy Governance Lambda Handler'
    response['Template'] = template
    response['Env'] = 'Environment Variables'

    return response

def deploy_template_handler(event, context):
    """ Lambda handler to handles the deployment
    of CloudFormation Templates

    Args:
        event (dict): event details from request
        context (dict): context of the lambda function

    Returns:
        response (dict): response built from handler
    """

    payload = event['Payload']
    cf_builder = CF_BUILDER()
    s3_cf = S3_CF(payload=payload)
    template = s3_cf.set_template()
    resource = s3_cf.get_template()
    
    if 'Description' in event:
        cf_builder.set_description(event['Description'])
    cf_builder.set_resources(
        resource_type='S3Bucket',
        resource=resource
    )
    template = cf_builder.get_template()

    if s3_cf.get_bucketname()['ResponseCode'] == 200:
        stackname = 's3-{}'.format(
            s3_cf.get_bucketname()['Message'])
        create_cloudformation(
            stack=stackname,
            template=template)

    response = {}
    response['Test'] = 'Deploy Lambda Handler'
    response['Template'] = template
    response['Env'] = 'Environment Variables'

    return response

def create_cloudformation(stack, template):
    """ Function that will create resources through a 
    CloudFormation Template

    Args:
        stack (str): name of the stack to create
        template (dict): cloud formation template to create
        env (dict): environment variables

    Returns:
        response (dict): based on boto3 request
    """
    if stack != '' and template != {}:
        client = boto3.client('cloudformation')
        response = client.create_stack(
            StackName=stack,
            TemplateBody=json.dumps(template)
        )
        return ok(response)
    return bad_request('CloudFormation template not provided')

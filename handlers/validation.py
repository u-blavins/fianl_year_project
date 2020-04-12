import json

from infrastructure_provisioner.cf_s3 import S3_CF
from infrastructure_provisioner.cf_builder import CF_BUILDER
from governance.governance import Governance


def validate_governed_payload_handler(event, context):
    """ Lambda handler to validate a payload, construct a
    CloudFormation template and apply governance checks

    Args:
        event (dict): event details from request
        context (dict): context of the lambda function

    Returns:
        response (dict): response built from handler
    """

    payload = event['Payload']
    env = event['Env']
    cf_builder = CF_BUILDER()
    s3_cf = S3_CF(payload=payload)
    s3_cf.set_template()
    resource = s3_cf.get_template()

    if 'Description' in event:
        cf_builder.set_description(event['Description'])
    cf_builder.set_resources(
        resource_type='S3Bucket',
        resource=resource
    )
    template = cf_builder.get_template()

    governance = Governance()
    governance.set_template(template=template)
    governance.get_resources()
    governance.validate()
    
    template = governance.get_template()

    response = {}
    response['Test'] = 'Validation Governance Lambda Handler'
    response['Template'] = template
    response['Env'] = env

    return response

def validate_payload_handler(event, context):
    """ Lambda handler to validate a payload and construct
    a CloudFormation template

    Args:
        event (dict): event details from request
        context (dict): context of the lambda function

    Returns:
        response (dict): response built from handler
    """

    payload = event['Payload']
    cf_builder = CF_BUILDER()
    s3_cf = S3_CF(payload=payload)
    s3_cf.set_template()
    resource = s3_cf.get_template()
    
    if 'Description' in event:
        cf_builder.set_description(event['Description'])
    cf_builder.set_resources(
        resource_type='S3Bucket',
        resource=resource
    )
    template = cf_builder.get_template()
    env = event['Env']

    response = {}
    response['Test'] = 'Validation Lambda Handler'
    response['Template'] = template
    response['Env'] = env

    return response
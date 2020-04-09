import json


def validate_governed_payload_handler(event, context):
    """ Lambda handler to validate a payload, construct a
    CloudFormation template and apply governance checks

    Args:
        event (dict): event details from request
        context (dict): context of the lambda function

    Returns:
        response (dict): response built from handler
    """

    template = event['Template']
    env = event['Env']

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

    template = event['Template']
    env = event['Env']

    response = {}
    response['Test'] = 'Validation Lambda Handler'
    response['Template'] = template
    response['Env'] = env

    return response
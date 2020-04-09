import json


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

    template = event['Template']

    response = {}
    response['Test'] = 'Deploy Lambda Handler'
    response['Template'] = template
    response['Env'] = 'Environment Variables'

    return response
import json


def returns_handler(event, context):
    """ Lambda handler to handle returns of the deployment
    of CloudFormation Templates

    Args:
        event (dict): event details from request
        context (dict): context of the lambda function

    Returns:
        response (dict): response built from handler
    """

    template = event['Template']

    response = {}
    response['Test'] = 'Return Lambda Handler'
    response['Template'] = template
    response['Env'] = event['Env']

    return response



def ok(message):
    """ Returns a response message 200 OK

    Args:
        message (str): message relating to status code raised

    Returns:
        Dictionary http response code
    """
    return {"ResponseCode": 200, "Message": message}


def created(message):
    """ Returns a response message 201 CREATED

    Args:
        message (str): message relating to status code raised

    Returns:
        Dictionary http response code
    """
    return {"ResponseCode": 201, "Message": message}


def bad_request(message):
    """ Returns a response message 400 BAD REQUEST

    Args:
        message (str): message relating to status code raised

    Returns:
        Dictionary http response code
    """
    return {"ResponseCode": 400, "Message": message}


def unauthorised(message):
    """ Returns a response message 401 UNAUTHORISED

    Args:
        message (str): message relating to status code raised

    Returns:
        Dictionary http response code
    """
    return {"ResponseCode": 401, "Message": message}


def not_found(message):
    """ Returns a response message 404 NOT FOUND

    Args:
        message (str): message relating to status code raised

    Returns:
        Dictionary http response code
    """
    return {"ResponseCode": 404, "Message": message}


def conflict(message):
    """ Returns a response message 409 CONFLICT

    Args:
        message (str): message relating to status code raised

    Returns:
        Dictionary http response code
    """
    return {"ResponseCode": 409, "Message": message}


def internal_server_error(message):
    """ Returns a response message 500 INTERNAL SERVER ERROR

    Args:
        message (str): message relating to status code raised

    Returns:
        Dictionary http response code
    """
    return {"ResponseCode": 500, "Message": message}

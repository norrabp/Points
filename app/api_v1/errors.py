""" Error Handling Endpoints """
from flask import jsonify
from ..exceptions import ValidationError
from . import api


@api.errorhandler(ValidationError)
def bad_request(e):
    """
    End point for a code 400 Bad Request error
    arguments:
        e: ValidationError instance
    returns:
        status code 400
        json with error message
    """
    response = jsonify({'status': 400, 'error': 'bad request',
                        'message': e.args[0]})
    response.status_code = 400
    return response


@api.app_errorhandler(404)  # this has to be an app-wide handler
def not_found(e):
    """
    Error not found handler
    arguments:
        e: Not used
    returns:
        status code 404
        json with error message
    """
    response = jsonify({'status': 404, 'error': 'not found',
                        'message': 'invalid resource URI'})
    response.status_code = 404
    return response


@api.errorhandler(405)
def method_not_supported(e):
    """
    Method not supported handler
    arguments:
        e: Not used
    returns:
        status code 405
        json with error message
    """
    response = jsonify({'status': 405, 'error': 'method not supported',
                        'message': 'the method is not supported'})
    response.status_code = 405
    return response

@api.app_errorhandler(500)  # this has to be an app-wide handler
def internal_server_error(e):
    """
    Internal Server Error handler
    arguments:
        e: Error raised by the server
    returns:
        status code 500
        json with error message
    """
    response = jsonify({'status': 500, 'error': 'internal server error',
                        'message': e.args[0]})
    response.status_code = 500
    return response
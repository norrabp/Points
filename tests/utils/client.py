import json
from urllib.parse import urlsplit, urlunsplit

class TestClient:
    """ Class holding methods for sending HTTP requests to the web server"""
    def __init__(self, app):
        self.app = app

    def send(self, url, method='GET', data=None, headers={}):
        """
        Send HTTP request to the web server for unit test
        arguments:
            self: current client object
            url: url to send HTTP request to
            method: which HTTP method to perform the request with
            data: data to send to server
            headers: headers sent server to determine response type
        returns:
            A response variable containing the server's response
            and the json object returned from the request
        """
        # for testing, URLs just need to have the path and query string
        url_parsed = urlsplit(url)
        url = urlunsplit(('', '', url_parsed.path, url_parsed.query,
                          url_parsed.fragment))

        # append the authentication headers to all requests
        headers = headers.copy()
        headers['Content-Type'] = 'application/json'
        headers['Accept'] = 'application/json'

        # convert JSON data to a string
        if data:
            data = json.dumps(data)

        # send request to the test client and return the response
        with self.app.test_request_context(url, method=method, data=data,
                                           headers=headers):
            rv = self.app.preprocess_request()
            if rv is None:
                rv = self.app.dispatch_request()
            rv = self.app.make_response(rv)
            rv = self.app.process_response(rv)
            return rv, json.loads(rv.data.decode('utf-8'))

    def get(self, url, headers={}):
        return self.send(url, 'GET', headers=headers)

    def post(self, url, data, headers={}):
        return self.send(url, 'POST', data, headers=headers)

    def put(self, url, data, headers={}):
        return self.send(url, 'PUT', data, headers=headers)

    def delete(self, url, headers={}):
        return self.send(url, 'DELETE', headers=headers)

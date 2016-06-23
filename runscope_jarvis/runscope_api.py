import logging
import requests
# import pdb
from pprint import pformat

LOGGER = logging.getLogger(__name__)


class RunscopeApi(object):

    def __init__(self, token, bucket_name):
        """Initialize with Runscope's Human-readable Bucket Name
        and config yaml"""
        self.api_base = 'https://api.runscope.com'
        self.session = self._prepare_session(token)
        self.bucket_key = self._get_bucket_key(bucket_name)
        self.available_tests = self._get_available_tests()

    def post(self, url, payload={}):
        response = self.session.post(url, data=payload)
        return self._handle(url, response)

    def get(self, url, payload={}):
        response = self.session.get(url, params=payload)
        return self._handle(url, response)

    def _prepare_session(self, token):
        session = requests.Session()
        session.headers.update({'Authorization': 'Bearer {}'.format(token)})
        return session

    def _get_bucket_key(self, bucket_name):
        """ Get + store bucket key from api """
        response = self.get(self.api_base + '/buckets')
        keys = [bucket['key'] for bucket in response['data'] if bucket['name'] == bucket_name]
        if len(keys):
            key = keys[0]
            return key
        else:
            return None # Maybe just raise TODO

    def _get_available_tests(self):
        parsed_tests = {}
        url = self.api_base + '/buckets/{key}/tests'.format(key=self.bucket_key)
        response = self.get(url)
        for test in response['data']:
            name = test['name']
            parsed_tests[name] = {
                'name': name, # might need name here too for pretty reporting
                'trigger_url': test['trigger_url'],
                'description': test['description'],
                'id': test['id']
            }
        return parsed_tests


    #  TODO might want to handle meta too
    @staticmethod
    def _handle(url, response):
        """check error property on response."""
        parsed_response = response.json()
        # LOGGER.debug(response)
        if parsed_response['error'] != None:
            LOGGER.exception(parsed_response['error'])
            # Maybe don't always raise
            raise Exception('Call to ' + url + ' returned error: See above')
        return parsed_response

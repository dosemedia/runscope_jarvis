import unittest
from types import *
import requests_mock
from runscope_jarvis.runscope_api import RunscopeApi
from tests.support import api_stubs

# class MyResponse(object):
#     def json(self):
#         return {'error': 'I stole your method'}
#
# requests.Session.get = MagicMock(return_value=MyResponse())

class RunscopeApiTest(unittest.TestCase):

    @requests_mock.Mocker()
    def setUp(self, m):
        """Set up a basic API config object"""
        m.get('https://api.runscope.com/buckets', json=api_stubs['buckets_index'])
        m.get('https://api.runscope.com/buckets/coolKey123/tests', json=api_stubs['tests_index'])
        self.test_api = RunscopeApi(token='Wheee', bucket_name='Cool Api')

    def tearDown(self):
        """Call after every test case."""

    # @unittest.skip('not tested yet')
    # def test_post_sends_post_with_payload_and_headers(self):
    #     assert False
    #
    # @unittest.skip('not tested yet')
    # def test_get_sends_get_with_params_and_headers(self):
    #     assert False
    #
    # @unittest.skip('not tested yet')
    # def test_handle_returns_json_for_good_response(self):
    #     assert False
    #
    # @unittest.skip('not tested yet')
    # def test_handle_raises_on_error(self):
    #     assert False
    #
    # @unittest.skip('not tested yet')
    # def test_get_available_tests_returns_tests_as_dict(self):
    #     assert False
    #
    # @unittest.skip('not tested yet')
    # def test_get_bucket_key_returns_key_as_string(self):
    #     assert False

if __name__ == "__main__":
    unittest.main() # run all tests

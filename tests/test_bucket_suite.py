import unittest
from types import *
import os
import yaml
import mock
from tests.support import api_stubs
from runscope_jarvis import BucketSuite, RunscopeApi

class BucketSuiteTest(unittest.TestCase):
    # def mock_api:
    #     class MockApi(RunscopeApi):

    import requests_mock

    @mock.patch('runscope_jarvis.runscope_api.RunscopeApi')
    def setUp(self, MockApi):
        """Set up a basic Suite object with mocked api"""
        # dirname = os.path.dirname(os.path.abspath(__file__))
        # config = dirname + '/support/example_config.yaml'
        # config = yaml.safe_load(config)
        mock_api = MockApi.return_value
        happy_config = {'bucket_name': 'Cool Api', 'test_plan': ['Test 1', 'Test 2']}
        missing_test_config = {'bucket_name': 'Bad Api', 'test_plan': ['Test 1', 'Missing Test']}
        target_url = 'https://api.internet.com' # technically required for RunscopeApi
        self.suites = {
            'happy': BucketSuite(
                config=happy_config,
                target_url=target_url,
                api=mock_api),

            'missing': BucketSuite(
                config=missing_test_config,
                target_url=target_url,
                api=mock_api)
        }
        mock_api.available_tests = {
            'Test 1': {
                'id': 'testid1',
                'name': 'Test 1',
                'trigger_url': 'https://api.runscope.com/radar/foo/trigger',
                'description': 'This is the first test description'
            },
            'Test 2': {
                'id': 'testid2',
                'name': 'Test 2',
                'trigger_url': 'https://api.runscope.com/radar/foo/trigger',
                'description': 'This is the Second test description'
            },
            'Test 3': {
                'id': 'testid3',
                'name': 'Test 3',
                'trigger_url': 'https://api.runscope.com/radar/foo/trigger',
                'description': 'This is the third test description'
            }
        }
        # req_mock.post('https://api.runscope.com/radar/foo/trigger',
        #         json=api_stubs['trigger_success'])
        # self.suite_config = self.suites['happy'].prepare_test_plan()
        # self.active_tests = self.suites['happy'].start_tests(self.suite_config)

    def tearDown(self):
        """Call after every test case."""

    def test_loads_correct_config_schema(self):
        """Suite object needs at least these things"""
        suite = self.suites['happy']
        # assert suite.suite_name
        assert suite.target_url
        assert suite.config.has_key('bucket_name')
        assert suite.config.has_key('test_plan')

    def test_prepare_test_plan_returns_filtered_test_list(self):
        suite = self.suites['happy']
        result = suite.prepare_test_plan()
        assert type(result) is ListType
        assert len(result) is len(suite.config['test_plan']), "result length is " + str(len(result))
        for config in result:
            assert type(config) is DictType, """actual type: """ + type(config)
            assert config.has_key('trigger_url')

    @unittest.skip('not tested yet')
    def test_prepate_test_plan_logs_test_plan(self):
        assert False

    def test_prepare_test_plan_raises_on_missing_test(self):
        """prepare_test_plan() compares available runscope tests
         with list in yml & raises if one is missing"""
        suite = self.suites['missing']
        with self.assertRaises(Exception) as context:
            suite.prepare_test_plan()
        self.assertTrue('Missing Test not found on Runscope' in context.exception)

    def test_start_tests_returns_list_of_active_test_data_from_api(self):
        """start_tests() should take a List of tests and map/return
        a list of active tests"""
        suite = self.suites['happy']
        suite.api.post.return_value = api_stubs['trigger_success']
        # suite.api.post
        # m.post('https://api.runscope.com/radar/foo/trigger',
        #         json=api_stubs['trigger_success'])
        suite_config = suite.prepare_test_plan()
        results = suite.start_tests(suite_config)
        for active_test in results:
            assert type(active_test) is DictType
            assert active_test.has_key('runs'), "response runs property contains List of test runs"

    @unittest.skip('assertions not working with this mocked api response')
    def test_await_results_collects_list_of_results(self):
        suite = self.suites['happy']

        suite_config = suite.prepare_test_plan()
        suite.api.post.return_value = api_stubs['trigger_success']
        active_tests = suite.start_tests(suite_config)
        suite.api.post.return_value = api_stubs['test_complete']
        results = suite.await_results(active_tests)
        # print results
        # for result in results:
            # assert isInstance(result.__class__, dict)
            # assert result.has_key('foo')

if __name__ == "__main__":
    unittest.main() # run all tests

import unittest
import logging
import time
import pdb
from pprint import pformat


LOGGER = logging.getLogger(__name__)

class BucketSuite(object):
    """reads from config to pull a suite config and initialize api"""
    def __init__(self, config, target_url, api):
        self.config = config
        self.target_url = target_url
        self.api = api

    def __call__(self):
        """run tests"""
        test_plan = self.prepare_test_plan()
        # LOGGER.info(pformat(test_plan))
        active_tests = self.start_tests(test_plan)
        # LOGGER.info(pformat(active_tests))
        results = self.await_results(active_tests)
        # LOGGER.info(pformat(results))
        self.assert_success(results)

    def prepare_test_plan(self):
        """Compare config test_plan with api available tests. Return filtered\
        config object."""
        test_plan = self.config['test_plan']
        available_tests = self.api.available_tests
        test_config = []
        verbal_plan = 'The following tests will run against {bucket} at {url}:\n'.format(
            bucket=self.config['bucket_name'],
            url=self.target_url)
        for test_name in test_plan:
            if test_name in available_tests:
                test = available_tests[test_name]
                test_config.append(test)
                verbal_plan += '{name}:\n\t{description}\n'.format(
                    name=test_name,
                    description=test['description'])
            else:
                LOGGER.debug(pformat(available_tests))
                error_message = '{test_name} not found on Runscope'.format(test_name=test_name)
                raise Exception(error_message)
        LOGGER.info('The following tests are selected to run:')
        for test in test_config:
            LOGGER.info(test['name'])
        return test_config

    def start_tests(self, config):
        """Initialize tests using config object. Return List of active tests."""
        active_tests = [self._trigger_test(test) for test in config]
        return active_tests

    def await_results(self, active_tests, timeout=120):
        """Converts active tests to a flattened list of runs, then iteratively checks them until timeout is reached"""
        results = []
        time_goal = time.time() + int(timeout)
        active_test_runs = self._flatten_runs(active_tests)
        LOGGER.debug('***active_test_run_length** ' + str(len(active_test_runs)))
        # LOGGER.debug(pformat('active_test_runs: ' + pformat(active_test_runs)))
        total_test_count = len(active_test_runs)
        while (len(active_test_runs) > 0) and (time.time() < time_goal):
            for run in active_test_runs:
                time.sleep(1)
                result = self._check_result(run)
                # LOGGER.debug(pformat(result))
                run['complete'] = (True if result else False)
                if result: results.append(result)
            active_test_runs = filter(lambda (run): run['complete'] == False, active_test_runs)
            # LOGGER.debug(len(results) + len(active_test_runs) == total_test_count)
            # LOGGER.debug('***active_test_runs length** ' + str(len(active_test_runs)))
            # LOGGER.debug(pformat(results))
        LOGGER.debug('test results: ' + pformat(results))
        return results

    def assert_success(self, results):
        if len(results) == 0: raise Exception('results are empty')
        for result in results:
            result_message = result['result']
            # assert result_message == 'pass', 'Test returned ' + result_message
        # would be nice to assert/return in a cleaner way.
        parsed_results = [{'view_results': self._test_result_web(result), 'result': result['result']} for result in results]
        fails = len(filter(lambda result: result['result'] != 'pass', parsed_results))
        for result in parsed_results:
            LOGGER.info('{res}: {url}'.format(res=result['result'].upper(), url=result['view_results']))
        assert(fails==0), str(fails) + ' tests failed. See log for details'
    # @staticmethod
    def _trigger_test(self, test_config):
        url = test_config['trigger_url']
        response = self.api.post(url, payload={'baseUrl':self.target_url})
        return response['data']

    def _check_result(self, run):
        # LOGGER.debug("Checking run:" + pformat(run))
        # LOGGER.debug('result URL: ' + url)
        response = self.api.get(self._test_result_api(run))
        # LOGGER.debug('Response: ' + pformat(response))
        if response['data']['finished_at']:
            # LOGGER.debug(response['data'])
            return response['data']
        return False


    # TODO this is attached to the api's bucket key
    def _test_result_web(self, test_run):
        url = ' https://www.runscope.com/radar/{bucket}/{test}/history/{run} '.format(
            bucket=self.api.bucket_key,
            test=test_run['test_id'],
            run=test_run['test_run_id'])
        # LOGGER.debug(url)
        return url

    def _test_result_api(self, test_run):
        url = 'https://api.runscope.com/buckets/{bucket}/tests/{test}/results/{run}'.format(
            bucket=self.api.bucket_key,
            test=test_run['test_id'],
            run=test_run['test_run_id'])
        # LOGGER.debug(url)
        return url

    @staticmethod
    def _flatten_runs(tests):
        test_runs = [ run for test in tests for run in test['runs'] ]
        # LOGGER.debug(pformat(tests))
        # LOGGER.debug(pformat(test_runs))
        # pdb.set_trace()
        return test_runs

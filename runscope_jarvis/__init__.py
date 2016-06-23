import os
import sys
import logging
import yaml

from bucket_suite import BucketSuite
from runscope_api import RunscopeApi


LOGGER = logging.getLogger(__name__)
# For dev purposes
logging.basicConfig(level=logging.INFO)

# other possible args like fast fail?
def main():
    """Execute runscope tests"""
    print sys.argv
    suite_name = sys.argv[1]
    target_url = sys.argv[2]

    yaml_file = 'runscope.yaml'
    config = _read_config(yaml_file)

    token = config['api_token']
    suite_config = config['suites'][suite_name]
    bucket_name = suite_config['bucket_name']

    api = RunscopeApi(token, bucket_name)
    suite = BucketSuite(
        target_url=target_url,
        config=suite_config,
        api=api)

    suite()

def jarvis():
    """Execute runscope tests in jenkins using ENV"""
    suite_name = os.environ['RUNSCOPE_SUITE']
    target_url = os.environ['RUNSCOPE_TARGET_URL']
    yaml_file = 'runscope_jarvis/runscope.yaml'
    config = _read_config(yaml_file)

    token = config['api_token']
    suite_config = config['suites'][suite_name]
    bucket_name = suite_config['bucket_name']
    api = RunscopeApi(token, bucket_name)
    suite = BucketSuite(
        target_url=target_url,
        config=suite_config,
        api=api)

    suite()

def _read_config(yaml_file):
    """Read config Yaml to python dict"""
    with open(yaml_file, 'rbU') as config_file:
        config = yaml.safe_load(config_file)
    return config

if __name__ == "__main__":
    """only for running on jarvis- otherwise use setup.py install-
     runs test suite"""
    jarvis()

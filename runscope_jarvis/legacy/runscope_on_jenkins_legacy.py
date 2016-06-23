import requests
import os
import time
import pprint
import sys
import yaml
#pylint: skip-file
#pylint: disable-all

# from requests_runscope import RunscopeAdapter

pp = pprint.PrettyPrinter(indent=2).pprint

# Runscope Api Base: https://api.runscope.com
# Personal Access Token: 7477f2d9-b058-44b0-9d03-37a7ad223473
# https://www.runscope.com/docs/api-testing/integrations
# Trigger url: https://api.runscope.com/radar/:trigger_id/trigger?runscope_environment=:environment_uuid
# Trigger all: GEThttps://api.runscope.com/radar/bucket/:trigger_id/trigger
# Get results by test run ID: /buckets/<bucket_key>/tests/<test_id>/results/<test_run_id>
# Ptolemy trigger url: https://api.runscope.com/radar/bucket/8efc9bf1-9b16-4628-8027-c6aee1a9f0ac/trigger


# BUCKET_KEYS = {
#     "hermes" : "8jgwscu0i1qv",
#     "ptolemy": "something"
#     #"ptolemy": {
#     # bucket_key: "some string"
#     # tests: [happy_path, bad_user_id, ] }
#     } # TODO: Fix this to get bucket key from api?
API_BASE = "https://api.runscope.com"
API_ACCESS_TOKEN = "7477f2d9-b058-44b0-9d03-37a7ad223473"
# TODO https://api.runscope.com/radar/bucket/4f5794f5-a6e0-4849-bdd9-d1e1d7009812/trigger


class RunscopeTest:
    def __init__(self, **payload_args):
        # TODO: these vars could also be set using a call to the api if we wanted to
        # specify test by name without knowing specific ids as in self.bucket_key= below
        try:
            # self.bucket_key = self.get_bucket_key(os.environ['BUCKET_NAME'])
            # TODO - WRITE METHOD TO FETCH BUCKET KEY BASED ON NAME
            self.bucket_key = BUCKET_KEYS[os.environ['BUCKET_NAME']]
            self.trigger_id = os.environ['TRIGGER_ID']
            self.environment_uuid = os.environ['ENVIRONMENT_UUID']
            self.base_url = os.environ['BASE_URL']
        except KeyError:
            raise Exception("TRIGGER_ID, ENVIRONMENT_UUID, BUCKET_NAME and"
                            "BASE_URL are required environment variables")
        self.request_payload = payload_args


    #   Removing some noise from the printout in comments below
    def trigger(self):
        print "Triggering test... "
        self.trigger_response = requests.get(self._trigger_url(), self.request_payload)
        if self._response_status() == 'success':
            self.test_run_id = self._test_run_info("test_run_id")
            self.test_id = self._test_run_info("test_id")
            print "Runscope test started- ID " + self.test_run_id
            print "View results: " + self._web_results_url()
            print
            return True
        else:
            pp(self.trigger_response.json())
            raise Exception("Runscope responded to test trigger with status '" + self._response_status() + "'")

    def call_api_for_results(self, timeout_secs, first_in=30, pause_between_checks=10):
        timeout = time.time() + int(timeout_secs)
        try_counter = 0
        session = requests.Session()
        session.mount(
            'https://api.runscope.com',
            )
        time.sleep(first_in)
        while True:
            if time.time() > timeout:
                raise Exception("The Runscope Test " + self.test_run_id +
                " didn't complete in time")
            try_counter += 1
            print "try " + str(try_counter) + "..."
            response = session.get(
                self._test_results_resource(),
                headers={"Authorization" : "bearer " + API_ACCESS_TOKEN}
                )
            res_dict = response.json()
            if res_dict[u'meta'][u'status'] == 'error':
                raise Exception("Error: " + res_dict[u'error'][u'message'])
            # import pdb; pdb.set_trace()
            if bool(res_dict[u'data'][u'finished_at']):
                result = res_dict[u'data'][u'result']
                print "TEST RESULT: " + result
                if (result == "pass"):
                    return True
                else:
                    pp(res_dict)
                    raise Exception("The test failed somewhere: " + result)
            time.sleep(pause_between_checks)

    def _web_results_url(self):
        url = (
            "https://www.runscope.com/radar/{bucket_key}/{test_id}/"
            "results/{test_run_id}"
        )
        return url.format(
                    bucket_key = self.bucket_key,
                    test_id = self.test_id,
                    test_run_id = self.test_run_id)

    def _response_status(self):
        return self.trigger_response.json()[u'meta'][u'status']

    def _test_results_resource(self):
        return (API_BASE + "/buckets/{bucket_key}/tests/{test_id}/"
        "results/{test_run_id}").format(
            bucket_key = self.bucket_key,
            test_id = self.test_id,
            test_run_id = self.test_run_id
            )


            # TODO: Test entire bucket w baseURL and other keys? https://api.runscope.com/radar/bucket/4f5794f5-a6e0-4849-bdd9-d1e1d7009812/trigger
    def _trigger_url(self):
        url = (
            "https://api.runscope.com/radar/{trigger_id}/trigger"
            "?runscope_environment={environment_uuid}"
            "&baseUrl={base_url}"
            )
        return url.format(
                    trigger_id = self.trigger_id,
                    environment_uuid = self.environment_uuid,
                    base_url = self.base_url)

    def _test_run_info(self, key_to_get):
        try:
            return self.trigger_response.json()[u'data'][u'runs'][0][key_to_get]
        except AttributeError:
            raise Exception("No trigger_response yet- did you trigger a test?")



def main():
    this_test = RunscopeTest()
    this_test.trigger()
    this_test.call_api_for_results(timeout_secs=120)



if __name__ == '__main__':
    main()


# ## Notes:
# * I used the runscope adapter (example below) for api calls following this pattern but don't think it is necessary- could mostly have been done with regular GET requests.
# * Don't know the best place to set env variables. This is designed to be usable with basically any runscope test
# * Don't like my use of globals and not sure of my design patterns or pythonic style. I'd be interested to hear your comments and to see how it ends up integrating with the build pipeline if you can use it.
# * We use a single application auth token rather than going through the oauth process which I believe is fine.
# * one issue which i believe is a bug on runscope- the environment_uuid param i set in the initial trigger url doesn't seem to work- it runs in the environment set as default even though the response I get back shows the correct environment_uuid. I might follow up with them on this but it doesn't affect the test working.
# * I wasn't consistent in my use of double/single quotes or the unicode-formatted strings. sorry

### Runscope api example
# def main():
#     session = requests.Session()
#     session.mount('http://', RunscopeAdapter("g3sgfmtyhvi0"))
#     session.mount('https://', RunscopeAdapter("g3sgfmtyhvi0"))

#     # for authenticated buckets (https://www.runscope.com/docs/buckets#authentication)
#     # session.mount('http://', RunscopeAdapter("g3sgfmtyhvi0", auth_token="abcd1234"))
#     # session.mount('https://', RunscopeAdapter("g3sgfmtyhvi0", auth_token="abcd1234"))

#     # for service regions (https://www.runscope.com/docs/regions)
#     # session.mount('http://', RunscopeAdapter("g3sgfmtyhvi0", gateway_host="eu1.runscope.net"))
#     # session.mount('https://', RunscopeAdapter("g3sgfmtyhvi0", gateway_host="eu1.runscope.net"))

#     payload = {'some': 'data'}

#     resp = session.post("https://yourapihere.com", data=payload)
#     print resp.content
# if __name__ == '__main__':
#     main()

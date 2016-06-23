Python package to run a suite of runscope tests- currently uses `runscope.yaml` in `/`

* python setup.py install
`runscope {suite, eg hermes_health} {target_url}`

*tests run against their default environment (set through the runscope ui). for clarity's sake i have been using the bucket-wide-settings as default with separate environments for QA, Prod etc.*

There are some assumptions built into this when running. First, your default environment should have all variables defined except for the `BaseUrl`, which will be overwritten in any case by the `TARGET_URL` when running in jarvis. Integrations with slack, newrelic, etc should also be configured for that default environment. Locations can also have an effect- specifically setting no locations will cause the test to exit outright, and setting multiple will cause the test to run from multiple locations. This should not affect jarvis' ability to parse and report all test results.

We currently assume a 120-second timeout for test completion. If a single test might take longer than that (since they run concurrently) we'll need to add a capability to set this timeout.

The runscope YAML file itself mostly is only interested in your `suite_name`s for jarvis and your Human-Readable test names (the literal test names from the runscope gui). Those should be consistent with their respective services.

If i think of anything else i'll be sure to let you know.



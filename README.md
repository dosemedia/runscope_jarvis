Python package to run a suite of runscope tests- currently uses `runscope.yaml` in your current working directory (see runscope.yaml.example in this repo)

## Usage
`:> runscope {suite} {base_url}`

```
  Example ./runscope.yaml:
  api_token: 'some-kind-of-token-from-runscope'
  suites:
    regression:
      bucket_name: 'Special Api' # Human-readable bucket name
      test_plan:
        - 'Happy Path' # Human-readable test name
        - 'Bad Encoding'
        - 'Empty Requests'
```
...
```
# Execute tests
:> runscope regression https://api.internet.com
// Your 'Special Api' bucket's tests named 'Happy Path,'
// 'Bad Encoding,' and 'Empty Requests' will execute
// simultaneously against the location https://api.internet.com
```
### Caveats and assumptions:
* The system under tests's location (api.internet.com above) will be passed into the Runscope variable {{baseUrl}}.
* tests run against their default environment (set through the runscope ui). Therefore:
  * All other variables should be set within the default test environment.  
  * Integrations with slack, newrelic, etc should also be configured for that default environment.
  * Locations can also have an effect- specifically setting no default locations will cause the test to exit immediately, and setting multiple will cause the test to run from multiple locations.
  * We currently assume a 120-second timeout for test completion. If a single test might take longer than that (since they run concurrently) the command will fail.

*This is currently a very much beta/0.9 build.*
### Possible future features might include:
* better error handling for incomplete input
* cleaner output/reporters
* Better api token obfuscation
* Ability to set timeout
* configuring test runs more flexibly from the cli, including:
  * Ability to set other variables
  * Ability to set test environment
  * Ability to forego YAML file altogether
  * Custom names for yaml file.
  

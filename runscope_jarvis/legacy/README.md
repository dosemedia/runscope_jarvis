# Runscope test and response shell script
trigger with 
```
TRIGGER_ID=2cfbcc0f-4f67-4917-ac71-97a64dce14dd ENVIRONMENT_UUID=eb373a4c-3d6b-4283-ba22-26e443e40552 BUCKET_NAME=hermes BASE_URL='http://hermes.01100100011011110111001101100101.com' python runscope_on_jenkins.py```

Currently requires a bunch of env variables as well as the following pip modules:
- requests
- os
- time
- pprint
- sys
- requests_runscope

This is my first time writing python so i can't remember which of these are part of the standard library ¯\_(ツ)_/¯



## Other Notes:
* I used the runscope adapter (example at bottom of script) for api calls following this pattern but don't think it is necessary- could mostly have been done with regular GET requests.
* Don't know the best place to set env variables. This is designed to be usable with basically any runscope test
* Don't like my use of globals and not sure of my design patterns or pythonic style. I'd be interested to hear your comments and to see how it ends up integrating with the build pipeline if you can use it.
* We use a single application auth token rather than going through the oauth process which I believe is fine.
* one issue which i believe is a bug on runscope- the environment_uuid param i set in the initial trigger url doesn't seem to work- it runs in the environment set as default even though the response I get back shows the correct environment_uuid. I might follow up with them on this but it doesn't affect the test working.
* I wasn't consistent in my use of double/single quotes or the unicode-formatted strings. sorry

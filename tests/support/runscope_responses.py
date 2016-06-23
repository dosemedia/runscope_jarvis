#pylint: skip-file
#pylint: disable-all

__doc__ = """TBD"""

api_stubs = {
    'trigger_success' : {
        u'error': None,
        u'meta': { u'status': u'success'},
        u'data': {
            u'runs_failed': 0,
            u'runs_started': 1,
            u'runs_total': 1,
            u'runs': [{
                u'agent': None,
                u'environment_id': u'eb373a4c-3d6b-4283-ba22-26e443e40552',
                u'environment_name': u'Jenkins',
                u'region': u'us3',
                u'status': u'init',
                u'test_id': u'this-is-a-test-id',
                u'test_name': u'Regression',
                u'test_run_id': u'this-is-a-test-run-id',
                u'test_run_url': u'https://www.runscope.com/radar/8jgwscu0i1qv/2b2d340b-cef0-4d81-9b6e-7cbf16d838fc/results/68285c4c-332e-40b6-a754-f42a78cad86e',
                u'test_url': u'https://www.runscope.com/radar/8jgwscu0i1qv/2b2d340b-cef0-4d81-9b6e-7cbf16d838fc',
                u'url': u'https://www.runscope.com/radar/8jgwscu0i1qv/2b2d340b-cef0-4d81-9b6e-7cbf16d838fc/results/68285c4c-332e-40b6-a754-f42a78cad86e',
                u'variables': {
                    u'baseURL': u'http://cool-api.dose.com',
                    u'caption': u'Cool Test.',
                }
            }]
        }
    },

    'buckets_index': {
        u'error': None,
        u'meta': { u'status': u'success'},
        u'data': [
            {
                'name': 'Cool Api',
                'key': 'CoolKey123'
            },
            {
                'name': 'Bad Api 1',
                'key': 'CoolKey123'
            }

        ]
    },
    'tests_index': {
        u'error': None,
        u'meta': { u'status': u'success'},
        u'data': [
            {
                'id': 'testid1',
                'name': 'Test 1',
                'trigger_url': 'https://api.runscope.com/radar/foo/trigger',
                'description': 'This is the first test description'
            },
            {
                'id': 'testid2',
                'name': 'Test 2',
                'trigger_url': 'https://api.runscope.com/radar/foo/trigger',
                'description': 'This is the Second test description'
            },
            {
                'id': 'testid3',
                'name': 'Test 3',
                'trigger_url': 'https://api.runscope.com/radar/foo/trigger',
                'description': 'This is the third test description'
            },

        ]
    },
    'suite_config': [
        {
            'id': 'testid1',
            'name': 'Test 1',
            'trigger_url': 'https://api.runscope.com/radar/foo/trigger',
            'description': 'This is the first test description'
        },
    ],
    'test_complete':{'error': None, 'meta': {'result': 'cool erik'}, 'data': {'result': 'pass'}}
}

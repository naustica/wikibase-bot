import pytest
from wikibot.databot import Wikibot
import os


@pytest.fixture
def set_env():
    os.environ['wikibase_instance_url'] = 'http://localhost:8181/w/api.php'
    os.environ['wikibase_username'] = 'Test@bot'
    os.environ['wikibase_pw'] = 'testpw'


class TestWikibot:

    def test_retrieve_credentials(self, set_env):
        bot = Wikibot()

        credentials = bot.retrieve_credentials()

        assert all(i is not None for i in credentials)

        del os.environ['wikibase_instance_url']
        del os.environ['wikibase_username']
        del os.environ['wikibase_pw']

        credentials = bot.retrieve_credentials()

        assert credentials == [None, None, None]

    def test_get_login_token(self, set_env, requests_mock):

        bot = Wikibot()

        data = {"query": {"tokens": {"logintoken": "test_login_token"}}}

        requests_mock.get(os.environ.get('wikibase_instance_url'),
                          json=data)

        r = bot.get_login_token(os.environ.get('wikibase_instance_url'))

        assert r == 'test_login_token'

    def test_login(self, set_env, requests_mock):

        bot = Wikibot()

        data = {}

        requests_mock.post(os.environ.get('wikibase_instance_url'),
                           json=data)

        r = bot.login(api_url=os.environ.get('wikibase_instance_url'),
                      token='test_login_token',
                      username=os.environ.get('wikibase_username'),
                      password=os.environ.get('wikibase_pw'))

        assert r == {}

    def test_get_csrf_token(self, set_env, requests_mock):

        bot = Wikibot()

        data = {"query": {"tokens": {"csrftoken": "test_csrftoken"}}}

        requests_mock.get(os.environ.get('wikibase_instance_url'),
                          json=data)

        r = bot.get_csrf_token(api_url=os.environ.get('wikibase_instance_url'))

        assert r == 'test_csrftoken'

    def test_write_entity(self, set_env, requests_mock):

        bot = Wikibot()

        html = '<pre class="api-pretty-content">{"response": "test"}</pre>'

        requests_mock.post(os.environ.get('wikibase_instance_url'),
                           text=html)

        r = bot.write_entity(api_url=os.environ.get('wikibase_instance_url'),
                             edit_token='test_csrftoken',
                             entity_type='property',
                             labels={'en': 'test label'},
                             descriptions={'en': 'test description'},
                             datatype='string')

        assert r == {"response": "test"}

    def test_write_statement(self, set_env, requests_mock):

        bot = Wikibot()

        data = {}

        requests_mock.post(os.environ.get('wikibase_instance_url'),
                           json=data)

        r = bot.write_statement(os.environ.get('wikibase_instance_url'),
                                edit_token='test_csrftoken',
                                subject_id='Q82445',
                                property_id='P31',
                                object_id='Q5')

        assert r == {}

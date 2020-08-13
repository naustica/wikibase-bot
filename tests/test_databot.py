import pytest
from wikibot.databot import Wikibot
import os
import requests


@pytest.fixture
def set_env():
    os.environ['wikibase_instance_url'] = 'http://localhost:8181/w/api.php'
    os.environ['wikibase_username'] = 'Test@bot'
    os.environ['wikibase_pw'] = 'testpw'


@pytest.fixture(scope='session')
def session():
    return requests.Session()


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
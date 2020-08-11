import requests
import os
import json
from typing import List


class Wikibot:

    """
    Extended implementation of:

    https://github.com/HeardLibrary/digital-scholarship/blob/master/code/wikibase/api/write-statements.py
    """

    def __init__(self):
        self.session = requests.Session()

    def retrieve_credentials(self) -> List[str]:

        endpoint_url = os.environ.get('wikibase_instance_url')
        username = os.environ.get('wikibase_username')
        password = os.environ.get('wikibase_pw')

        return [endpoint_url, username, password]

    def get_login_token(self, api_url: str) -> str:
        parameters = dict(
            action='query',
            meta='tokens',
            type='login',
            format='json'
        )

        r = self.session.get(url=api_url, params=parameters)
        data = r.json()
        return data['query']['tokens']['logintoken']

    def login(self, api_url: str, token: str,
              username: str, password: str):
        parameters = dict(
            action='login',
            lgname=username,
            lgpassword=password,
            lgtoken=token,
            format='json'
        )
        r = self.session.post(api_url, data=parameters)
        data = r.json()

        return data

    def get_csrf_token(self, api_url: str) -> str:
        parameters = dict(
            action='query',
            meta='tokens',
            format='json'
        )

        r = self.session.get(url=api_url, params=parameters)
        data = r.json()

        return data['query']['tokens']['csrftoken']

    def write_property(self, api_url: str, edit_token: str, label_value: str,
                       description_value: str, datatype: str) -> int:
        parameters = dict(
            action='wbeditentity',
            bot=1,
            token=edit_token,
            new='property',
            data=json.dumps(dict(labels=dict(
                en=dict(
                    language='en',
                    value=label_value
                )
            ),
                descriptions=dict(
                en=dict(
                    language='en',
                    value=description_value
                )
            ),
                datatype=datatype
            ))
        )

        r = self.session.post(api_url, data=parameters)
        return r.status_code

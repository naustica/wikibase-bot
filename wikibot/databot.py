import requests
import os
import json
from typing import List, Dict
from bs4 import BeautifulSoup


class Wikibot:

    """
    Extended implementation of:

    https://github.com/HeardLibrary/digital-scholarship/blob/master/code/wikibase/api/write-statements.py
    """

    def __init__(self):
        self.session = requests.Session()

    def retrieve_credentials(self) -> List[str]:
        """
        Returns
        -------
        List[str]
            Information on bot credentials.
        """

        endpoint_url = os.environ.get('wikibase_instance_url')
        username = os.environ.get('wikibase_username')
        password = os.environ.get('wikibase_pw')

        return [endpoint_url, username, password]

    def get_login_token(self, api_url: str) -> str:
        """
        Parameters
        ----------
        api_url: str
            Url to the Wikibase API instance.

        Returns
        -------
        str
            Login token
        """
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
        """
        Parameters
        ----------
        api_url: str
            Url to the Wikibase API instance.
        token: str
            Your login token.
        username: str
            Your Wikibase bot username.
        password: str
            Your wikibase bot password.

        Returns
        -------
        JSON object
        """
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
        """
        api_url: str
            Url to the Wikibase API instance.

        Returns
        -------
        str
            CSRF Token
        """
        parameters = dict(
            action='query',
            meta='tokens',
            format='json'
        )

        r = self.session.get(url=api_url, params=parameters)
        data = r.json()

        return data['query']['tokens']['csrftoken']

    def write_entity(self, api_url: str, edit_token: str, entity_type: str,
                     labels: Dict[str, str], descriptions: Dict[str, str],
                     datatype: str = None, id: str = None,
                     aliases: Dict[str, str] = None):
        """
        This method creates a single new Wikibase entity and modifies it with
        serialised information.

        Parameters
        ----------
        api_url: str
            Url to the Wikibase API instance.
        edit_token: str
            CSRF token which can be generated with the get_crsf_token method.
        entity_type: str
            Type of entity to be created.
        labels: Dict[str, str]
            Label value of entity.
        descriptions: Dict[str, str]
            Description value of entity.
        datatype: str
            If entity type is set to property, specify the desired datatype.
        id: str
            Id of an existing entity type to be modified.
        aliases: Dict[str, str]
            Set an alias for an entity.

        Returns
        -------
        JSON object
        """

        data = {'labels': {}, 'descriptions': {}, 'aliases': {}}

        for k, v in labels.items():
            data['labels'].update({k: {'language': k, 'value': v}})

        for k, v in descriptions.items():
            data['descriptions'].update({k: {'language': k, 'value': v}})

        if aliases:
            for k, v in aliases.items():
                data['aliases'].update({k: {'language': k, 'value': v}})
        else:
            data.pop('aliases')
        if entity_type == 'property':
            data.update({'datatype': datatype})

        parameters = dict(
            action='wbeditentity',
            bot=1,
            token=edit_token,
            new=entity_type,
            data=json.dumps(data)
        )

        if id:
            parameters.pop('new')
            parameters.update({'id': id})

        r = self.session.post(api_url, data=parameters)
        r_html = BeautifulSoup(r.text, 'lxml')
        return json.loads(r_html.find('pre',
                                      {'class': 'api-pretty-content'}).string)

    def write_statement(self, api_url: str, edit_token: str,
                        subject_id: str, property_id: str, object_id: str):

        """
        This method creates a wikibase claim.

        Parameters
        ----------
        api_url: str
            Url to the Wikibase API instance.
        edit_token: str
            CSRF token which can be generated with the get_crsf_token method.
        subject_id: str
            Id of the entity the claim is being added to
        property_id: str
            Id of the property
        object_id: str
            Id of the object

        Returns
        -------
        JSON object
        """

        parameters = dict(
            action='wbcreateclaim',
            format='json',
            entity=subject_id,
            snaktype='value',
            bot=1,
            token=edit_token,
            property=property_id,
            value=json.dumps(
                {
                    'entity-type': 'item',
                    'numeric-id': object_id[1:]
                }
            )
        )

        r = self.session.post(api_url, data=parameters)

        return r.json()

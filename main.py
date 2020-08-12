from wikibot.databot import Wikibot
import pandas as pd

bot = Wikibot()

url, user, pw = bot.retrieve_credentials()

login_token = bot.get_login_token(url)
print(f'Login token: {login_token}')

login = bot.login(url, login_token, user, pw)
print(f'Confirm login: {login}')

csrf_token = bot.get_csrf_token(url)
print(f'CSRV token: {csrf_token}')

df = pd.read_csv('wikidata-properties-complete-en.tsv', sep='\t')

for idx, row in df.iterrows():
    mapper = {
        'http://wikiba.se/ontology#CommonsMedia': 'commonsMedia',
        'http://wikiba.se/ontology#String': 'string',
        'http://wikiba.se/ontology#ExternalId': 'external-id',
        'http://wikiba.se/ontology#WikibaseItem': 'wikibase-item',
        'http://wikiba.se/ontology#Quantity': 'quantity',
        'http://wikiba.se/ontology#Time': 'time',
        'http://wikiba.se/ontology#Url': 'url',
        'http://wikiba.se/ontology#Monolingualtext': 'monolingualtext',
        'http://wikiba.se/ontology#WikibaseProperty': 'wikibase-property',
        'http://wikiba.se/ontology#TabularData': 'tabular-data',
        'http://wikiba.se/ontology#GeoShape': 'geo-shape',
        'http://wikiba.se/ontology#GlobeCoordinate': 'globe-coordinate'
    }

    property_type = mapper.get(row['propertyType'])

    if not property_type:
        print(f"Property type of: {row['property']} is unknown.")
        continue

    data = bot.write_entity(api_url=url,
                            edit_token=csrf_token,
                            new='property',
                            label_value=row['propertyLabel'],
                            description_value=row['propertyDescription'],
                            lang='en',
                            datatype=property_type)

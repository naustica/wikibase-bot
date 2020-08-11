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
    property_type = row['propertyType'].replace('http://wikiba.se/ontology#',
                                                '').lower()

    bot.write_property(url, csrf_token, row['propertyLabel'],
                       row['propertyDescription'], property_type)

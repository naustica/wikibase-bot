# wikibase-bot

[![Build Status](https://travis-ci.org/naustica/wikibase-bot.svg?branch=master)](https://travis-ci.org/github/naustica/wikibase-bot)
[![codecov.io](https://codecov.io/gh/naustica/wikibase-bot/branch/master/graph/badge.svg)](https://codecov.io/gh/naustica/wikibase-bot?branch=master)

This repository contains an extended implementation of this [wikibase-bot](https://github.com/HeardLibrary/digital-scholarship/blob/master/code/wikibase/api/write-statements.py) that is maintained by Digital Scholarship and Communications.

## Features

- Import of properties
- Import of items
- Adding of statements
- More features in pipeline!

## Installation

Download code by using

```bash
git clone https://github.com/naustica/wikibase-bot.git
```

### Requirements

The Code has been tested with Python 3.7. Besides, make sure you have installed the following packages.

- [requests](https://github.com/psf/requests)
- [pandas](https://github.com/pandas-dev/pandas)
- [beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/)
- [lxml](https://github.com/lxml/lxml)

## Configuration

This guide assumes that you already setup a wikibase instance. If not, visit this [page](http://learningwikibase.com/install-wikibase/). In addition, you will need to create a wikibase bot account to make this code work.

### Create a bot account

For a more detailed description on how to create a wikibase bot account visit this [page](https://heardlibrary.github.io/digital-scholarship/host/wikidata/bot/).

###### Steps:

1. In your local wikibase instance, go to Special pages
2. Under section "Users and rights", search for "Bot passwords"
3. Create your bot.
4. Save your credentials.

### Configure bot

Once you created your bot account, export the necessary environment variables via terminal.

```bash
export wikibase_instance_url=your-wikibase-url/w/api.php
export wikibase_username=your-wikibase-bot-username
export wikibase_pw=your-wikibase-bot-password
```

### Start bot

Type the following line to run the bot.

```bash
python main.py
```

## Import properties into any Wikibase instance

When launching a fresh installed Wikibase Docker instance, you will probably encounter an empty database. This bot helps you to import basic properties into your wikibase. For that, just export a tsv-file containing property lables and description from e.g. Wikidata (you can use this [query](https://w.wiki/ZJN)) and feed this bot.

```python
from wikibot.databot import Wikibot
import pandas as pd

bot = Wikibot()

url, user, pw = bot.retrieve_credentials()

login_token = bot.get_login_token(url)

login = bot.login(url, login_token, user, pw)
print(f'Confirm login: {login}')

csrf_token = bot.get_csrf_token(url)

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

    bot.write_entity(api_url=url,
                     edit_token=csrf_token,
                     entity_type='property',
                     label_value=row['propertyLabel'],
                     description_value=row['propertyDescription'],
                     lang='en',
                     datatype=property_type)
```

## Import items

You can also use the same method to create a wikibase item.

```python
bot.write_entity(api_url=url,
                 edit_token=csrf_token,
                 entity_type='item',
                 label_value='Henri de Toulouse-Lautrec',
                 description_value='French painter',
                 lang='en',
                 alias_value='Henri de Toulouse Lautrec')
```

## Overwrite existing item/property

By adding the parameter `id`, you can update an existing wikibase item or property.

```python
bot.write_entity(api_url=url,
                 edit_token=csrf_token,
                 entity_type='item',
                 label_value='Henri de Toulouse-Lautrec',
                 description_value='French painter',
                 lang='en',
                 id='Q82445')
```

## Write statement

Use the method `write_statement` to add statements into your database.

```python
bot.write_statement(api_url=url,
                    edit_token=csrf_token,
                    subject_id='Q82445',
                    property_id='P31',
                    object_id='Q5')
```

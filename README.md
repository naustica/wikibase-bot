# wikibase-bot

This repository contains an extended implementation of this [wikibase-bot](https://github.com/HeardLibrary/digital-scholarship/blob/master/code/wikibase/api/write-statements.py) that is maintained by Digital Scholarship and Communications.

## Features

- Import properties
- more features in pipeline!

## Installation

Download code by using

```bash
git clone https://github.com/naustica/wikibase-bot.git
```

### Requirements

Code has been tested with Python 3.7. Besides, make sure you have installed the following packages.

- [requests](https://github.com/psf/requests)
- [pandas](https://github.com/pandas-dev/pandas)

## Configuration

This guide assumes that you already have setup a wikibase instance. If not, visit this [page](https://semlab.io/howto/wikibase_basic). In addition, you will need to create a wikibase bot account to make this code works.

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
export wikibase_instance_url=your-wikibase-url
export wikibase_username=your-wikibase-bot-username
export wikibase_pw=your-wikibase-bot-password
```

### Start bot

Type the following line to run the bot.

```bash
python main.py
```

## Import properties into any Wikibase instance

When launching a fresh installed Wikibase Docker instance, you will probably encounter an empty database. This bot helps you to import basic properties into your wikibase. For that, just export a csv-File containing property lables and description from e.g. Wikidata (you can use this [query](https://w.wiki/ZJN)) and feed this bot.

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
    property_type = row['propertyType'].replace('http://wikiba.se/ontology#',
                                                '').lower()

    bot.write_property(url, csrf_token, row['propertyLabel'],
                       row['propertyDescription'], property_type)
```

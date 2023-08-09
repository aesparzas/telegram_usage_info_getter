# Telegram Usage Info Getter

Script to output in csv format relevant information about a telegram channel/group, its usage and its users, using Telethon, YML and CSV files

## How it works

This is a very simple scrip that interacts with the telegram API using Telethon, using the settings stableshed in the `config/config.yml` file and outputs a CSV with relevant user and usage information.

#### Setting up

For interacting with Telegram's API, you first need to register a new App going to [My Telegram](https://my.telegram.org/)
and going to "API development tools". After logging in and filling the App form you should have the `api id` and the `api hash

Both are needed in the `config/config.yml` file that should look like this:

```yaml
app_id: xxxxxxxx # numeric id for the telegram's app
api_hash: 'xxxxxxxxxxxxxxxxxxxxxxxx' # hexadecimal hash for using telegram's API
entities: # channels or groups ids or urls, they can be numeric ids or links
  - xxxxxxxxxxxx
  - 'https://t.me/xxxx'
extra_user_info: # boolean indicating if user info is needed
min_date: '' # minimum send date of messages in isoformat
max_date: '' # maximum send date of messages in isoformat
```

#### Running the script

Using a python virtual environment is widely recomended. The steps for setting it up and running the script are the following:

This steps are for setting the environment and are just needed once.

`python -m venv venv`

`. venv/bin/activate`

`pip install -r requiurements.txt`

For running the script.

`. venv/bin/activate`

`python py/telegram_usage/getter.py`

#### Output for messages

In the CSV named `<channel name>messages.csv` you can find the following columns:

 - id: the Telegram message id
 - from_id: the sender Telegram user id
 - fwd_from: it is not null if the message was forwarded from another id
 - reply_to: it is not null if the message is a reply to some other message
 - date: timestamp of when the message was created
 - has_media: true if the message had media attached to it
 - has_reactions: reaction count of the message
 - replies: reply count of the message
 - sender_id: same as from_id
 - sender_verified: boolean that indicates if the sender's user has been verified or not
 - sender_restricted: boolean that indicates if the sender's user has been restricted or not
 - sender_fake: boolean that indicates if the sender's user has been qualified as fake or not
 - sender_first_name: sender's user registered first name
 - sender_last_name: sender's user registered last name
 - sender_username: sender's user registered username
 - sender_phone: sender's user registered phone if visible

NOTE: the columns with the prefix `sender_` are only in the output if extra_user_info is set to true in the `config/config.yml` file

#### Output for Users

Afile with the following data called `<chanel name>users.csv` is only created if extra_user_info is set to true in the `config/config.yml` file,
and it has info from current users of channel or group.

 - id: same as from_id
 - verified: boolean that indicates if the user has been verified or not
 - restricted: boolean that indicates if the user has been restricted or not
 - fake: boolean that indicates if the user has been qualified as fake or not
 - first_name: user registered first name
 - last_name: user registered last name
 - username: user registered username
 - phone: user registered phone if visible

## Built With

* [PyYml](https://pypi.org/project/PyYAML/) - YAML parser and emitter for Python
* [Telethon](https://docs.telethon.dev/en/stable/) - Library is meant to make it easy for you to write Python programs that can interact with Telegram. 

## Authors

* **Adolfo Esparza** - [aesparzas](https://github.com/aesparzas)

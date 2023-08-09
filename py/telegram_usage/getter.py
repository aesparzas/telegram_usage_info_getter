import csv
import datetime

import telethon.tl.types
import yaml
from telethon import TelegramClient


output_message_file = 'messages.csv'
output_users_file = 'users.csv'


with open('config/config.yml', 'r') as file:
    configs = yaml.load(file, yaml.FullLoader)
app_id = configs.get('app_id')
api_hash = configs.get('api_hash')
entities = configs.get('entities')
extra_user_info = configs.get('extra_user_info')
min_date = configs.get('min_date')
min_date = datetime.date.fromisoformat(min_date) if min_date else None
max_date = configs.get('max_date')
max_date = datetime.date.fromisoformat(max_date) if max_date else None

client = TelegramClient('reader', app_id, api_hash)
client.start()


dict_keys = [
    'id', 'from_id', 'fwd_from', 'reply_to', 'date', 'media', 'reactions',
    'replies'
]
user_info = [
    'id', 'verified', 'restricted', 'fake', 'first_name', 'last_name', 'username',
    'phone', 'participant'
]


async def explore_messages():
    fieldnames = dict_keys
    if extra_user_info:
        fieldnames += ['sender_' + f for f in user_info]
    for entity in entities:
        channel = await client.get_entity(entity)

        await get_messages_csv_btw_dates(channel, fieldnames, min_date, max_date)
        if extra_user_info:
            await get_users_csv(channel)


def get_plain(key, value):
    if key == 'participant':
        try:
            return value.date.isoformat()
        except:
            return ''
    if key == 'reactions':
        count = 0
        if hasattr(value, 'results') and isinstance(value.results, list):
            count = sum([r.count for r in value.results])
        return count
    if key == 'media':
        return value is not None
    if isinstance(value, datetime.datetime):
        return value.isoformat()
    if isinstance(value, telethon.tl.types.PeerUser):
        return value.user_id
    if isinstance(value, telethon.tl.types.MessageReplies):
        return value.replies
    if isinstance(value, telethon.tl.types.MessageFwdHeader):
        return value.channel_post
    if isinstance(value, telethon.tl.types.MessageReplyHeader):
        return value.reply_to_msg_id

    return value or ''


async def get_messages_csv_btw_dates(channel, fieldnames,  min_date=None, max_date=None):
    with open(channel.title + output_message_file, 'w') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        posts = client.iter_messages(channel)
        async for message in posts:
            if min_date and message.date.date() < min_date:
                break
            if max_date and message.date.date() >= max_date:
                continue
            dict_row = {k: get_plain(k, v)
                        for k, v in message.__dict__.items() if k in dict_keys}
            if extra_user_info and message._sender:
                dict_row.update({
                    'sender_' + k: getattr(message._sender, k) for k in user_info
                })

            writer.writerow(dict_row)


async def get_users_csv(channel):
    with open(channel.title + output_users_file, 'w') as file:
        writer = csv.DictWriter(file, fieldnames=user_info)
        writer.writeheader()
        participants = await client.get_participants(channel)
        for participant in participants:
            writer.writerow({k: get_plain(k, v)
                             for k, v in participant.__dict__.items()
                             if k in user_info})


client.loop.run_until_complete(
    explore_messages()
)
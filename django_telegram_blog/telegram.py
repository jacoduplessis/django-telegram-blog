from hashlib import md5

from django.conf import settings

from .models import Blog, Entry
from datetime import datetime, timezone
import json
import logging
from requests import Session
from io import BytesIO

logger = logging.getLogger(__name__)
session = Session()


def get_message_type(message):
    for choice, _ in Entry.TYPE_CHOICES:
        if choice in message:
            return choice


def get_message(update):
    if 'message' in update:
        return update['message']
    elif 'edited_message' in update:
        return update['edited_message']
    return None


def process_update(update):
    logger.debug("processing update")
    message = get_message(update)
    chat, user = message['chat'], message['from']
    if chat is None:
        logger.info(f'Received update that cannot be processed: {update}')
        return
    chat_id = chat.get('id')
    chat_name = chat.get('username') or chat.get('title') or chat.get('first_name') or chat_id
    blog, created = Blog.objects.get_or_create(
        telegram_chat_id=chat_id,
        defaults={
            'title': chat_name,
        }
    )

    if created:
        logger.debug(f'Created blog TG ID: {chat_id}')

    message_type = get_message_type(message)

    entry = Entry.objects.create(
        blog=blog,
        telegram_update_id=update['update_id'],
        update=json.dumps(update),
        type=message_type,
        message_time=datetime.fromtimestamp(message['date'], tz=timezone.utc)
    )

    entry.save_media_files()


def request(method, params):
    token = get_bot_token()
    url = f"https://api.telegram.org/bot{token}/{method}"
    r = session.post(url, params=params)
    r.raise_for_status()
    return r.json()


def get_bot_token():
    token = getattr(settings, 'TELEGRAM_BLOG_BOT_TOKEN')  # type: str
    if token is None:
        raise RuntimeError('TELEGRAM_BLOG_BOT_TOKEN settings is empty')
    return token


def get_webhook_url():
    token = get_bot_token()
    return md5(token.encode()).hexdigest()


def get_telegram_file_download_link(file_id):
    data = request('getFile', params=dict(file_id=file_id))
    file_path = data['result']['file_path']
    token = get_bot_token()
    return f'https://api.telegram.org/file/bot{token}/{file_path}'


def get_telegram_file_content(file_id):
    url = get_telegram_file_download_link(file_id)
    r = session.get(url)
    r.raise_for_status()
    return BytesIO(r.content)

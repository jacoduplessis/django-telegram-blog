from hashlib import md5
from urllib.parse import urljoin

from django.conf import settings
from django.urls import reverse

from requests import Session, RequestException
import logging


logger = logging.getLogger(__name__)

session = Session()


def get_bot_token():
    token = getattr(settings, 'TELEGRAM_BLOG_BOT_TOKEN')  # type: str
    if token is None:
        raise RuntimeError('TELEGRAM_BLOG_BOT_TOKEN setting is empty')
    return token


def get_webhook_hash():
    token = get_bot_token()
    return md5(token.encode()).hexdigest()


def get_webhook_path():
    return reverse('telegram_blog:webhook')


def get_webhook_url():
    base_url = getattr(settings, 'TELEGRAM_BLOG_URL')
    if base_url is None:
        raise RuntimeError('TELEGRAM_BLOG_URL setting is empty')
    return urljoin(base_url, get_webhook_path())


def request(method, data=None):
    token = get_bot_token()
    url = f"https://api.telegram.org/bot{token}/{method}"
    r = session.post(url, data=data)
    try:
        r.raise_for_status()
    except RequestException:
        logger.exception(r.content)
    return r.json()

from django.apps import AppConfig
from django.conf import settings
from telegram_blog.utils import request
from .utils import get_webhook_url

import logging

logger = logging.getLogger(__name__)


class TelegramBlogConfig(AppConfig):
    name = 'telegram_blog'

    def ready(self):

        if getattr(settings, 'TELEGRAM_BLOG_USE_WEBHOOK'):

            max_connections = getattr(settings, 'TELEGRAM_BLOG_WEBHOOK_MAX_CONNECTIONS', 40)
            webhook_url = get_webhook_url()
            data = request('getWebhookInfo').get('result')
            logger.info(f'existing webhook: {data}')
            if data['url'] != webhook_url or data['max_connections'] != max_connections:
                logger.info(f'setting webhook with url {webhook_url} and max connections: {max_connections}')
                response = request('setWebhook', {
                    'url': webhook_url,
                    'max_connections': max_connections
                })
                logger.info(f'setWebhook response: {response}')
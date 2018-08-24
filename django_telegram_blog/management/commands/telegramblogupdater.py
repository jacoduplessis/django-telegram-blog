from django.core.management.base import BaseCommand
from django_telegram_blog.telegram import process_update, session, get_bot_token
from django.conf import settings


class Command(BaseCommand):
    help = 'Connect to Telegram with long polling'

    def handle(self, *args, **options):

        offset = 0
        token = get_bot_token()

        url = f"https://api.telegram.org/bot{token}/getUpdates"

        if settings.DEBUG:
            # self.stdout.write(session.get(f"https://api.telegram.org/bot{token}/getMe").text)
            pass

        while True:
            r = session.get(url, params=dict(timeout=60, offset=offset+1))
            r.raise_for_status()
            response = r.json()
            if not response.get('ok'):
                self.stdout.write(response.get('description'))

            for update in response.get('result'):
                update_id = update.get('update_id')
                offset = max(update_id, offset)
                process_update(update)

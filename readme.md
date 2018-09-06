# Django Telegram Blog


### Getting Started

```
pip install django-telegram-blog
```

In `settings.py`:

```
TELEGRAM_BLOG_BOT_TOKEN = os.getenv('TELEGRAM_BLOG_BOT_TOKEN', '123')
TELEGRAM_BLOG_USE_WEBHOOK = False
TELEGRAM_BLOG_URL = 'https://example.com'  # base URL if using webhooks
TELEGRAM_BLOG_WEBHOOK_MAX_CONNECTIONS = 40  # see Telegram docs
```

In `urls.py`:

```
urlpatterns = [
   ...,
   path('/blog/', include('telegram_blog.urls')), 
]
```

Each chat that communicates with the bot will create a new `Blog` model.

Each message sent creates a new `Entry` model.

### Getting Updates

You have two choices:

1. Run `manage.py telegramblogupdater`. This is intended to ease developement but can be used in production.
2. Run the app on a publicly accessible HTTPS URL (use ngrok for dev) and run `manage.py telegramblogsetwebhook`.

### To Do

- entry deletion
- no webp/sticker in firefox
- group without message (created on bot add) does not have attr message_time
- file storage as celery task
- urlize filter should add target="_blank"
- keep original message time for edited messages

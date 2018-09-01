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

1. run `manage.py telegramblogupdater`. This is intented to ease developement but can be used
in production.
2. set `TELEGRAM_BLOG_USE_WEBHOOK = True` in settings and run `manage.py telegramblogsetwebhook`. You need to run
a webserver with SSL to use this, or use a tool like ngrok (for testing).

### To Do

- entry deletion
- no webp/sticker in firefox
- django admin
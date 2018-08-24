# Django Telegram Blog


### Getting Started

In `settings.py`:

```
TELEGRAM_BLOG_BOT_TOKEN = os.getenv('TELEGRAM_BLOG_BOT_TOKEN', '123')
```

In `urls.py`:

```
urlpatterns = [
   ...,
   path('/blog/', include('django_telegram_bot.urls')), 
]
```

Each chat that communicates with the bot will create a new `Blog` model.

Each message sent creates a new `Entry` model.
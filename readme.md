# Django Telegram Blog

Running example: [https://reports.hartebees.co.za](https://reports.hartebees.co.za).

To add content, simply start chatting to [@VoxPopBot](https://t.me/VoxPopBot) on Telegram.

### Getting Started

```
pip install django-telegram-blog
```

In `settings.py`:

```
TELEGRAM_BLOG_BOT_TOKEN = os.getenv('TELEGRAM_BLOG_BOT_TOKEN', '123')
TELEGRAM_BLOG_URL = 'https://example.com'  # base URL if using webhooks
TELEGRAM_BLOG_WEBHOOK_MAX_CONNECTIONS = 40  # see Telegram docs
```

To run the frontend, you need to set the `telegram_blog.urls` as the URL conf for the incoming
request. This can be done using middleware and setting the `request.urlconf` attribute. 

> The reason for this is that this project was originally created for hosting 
> on a subdomain of a Django instance and setting the `urlconf`
> attribute does not work when using URL namespaces.

Each chat that communicates with the bot will create a new `Blog` model.

Each message sent creates a new `Entry` model.



### Getting Updates

You have two choices:

1. Run `manage.py telegramblogupdater`. This is intended to ease developement but can be used in production.
2. Run the app on a publicly accessible HTTPS URL (use ngrok for dev) and run `manage.py telegramblogsetwebhook`.

### To Do

- entry deletion (login via Telegram Command?)
- no webp/sticker in firefox
- file storage as celery task
- urlize filter should add target="_blank"
- analytics
- update profile pic after change

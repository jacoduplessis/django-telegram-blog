from setuptools import setup



setup(
    name="django-telegram-blog",
    version="0.0.1",
    license="MIT",
    description="Blogging for Django via Telegram",
    author="Jaco du Plessis",
    author_email="jaco@jacoduplessis.co.za",  # SEE NOTE BELOW (*)
    packages=['django_telegram_blog'],
    package_data={
        'django_telegram_blog': [
            'template/*.html',
            'static/*.js',
        ]
    },
    install_requires=[
        "django",
        "requests",
    ],
)
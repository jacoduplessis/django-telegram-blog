from django.urls import path
from django.conf import settings
from . import views
from telegram_blog.utils import get_webhook_hash

# from telegram_blog.telegram import get_webhook_url

urlpatterns = [
    path('', views.Index.as_view(), name="index"),
    path('<int:pk>/', views.BlogDetailView.as_view(), name='blog_detail'),
]

if getattr(settings, 'TELEGRAM_BLOG_USE_WEBHOOK'):
    urlpatterns += [
        path('webhook/'+get_webhook_hash()+'/', views.WebhookView.as_view(), name='webhook'),
    ]

app_name = 'telegram_blog'
from django.urls import path
from . import views
from django_telegram_blog.telegram import get_webhook_url

urlpatterns = [
    path('', views.Index.as_view(), name="index"),
    path('<int:pk>/', views.BlogDetailView.as_view(), name='blog_detail'),
    # path(get_webhook_url(), views.WebhookView.as_view(), name="webhook"),
]

app_name = 'django_telegram_blog'
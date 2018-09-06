from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from telegram_blog.urls import urlpatterns as app_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
] + app_patterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

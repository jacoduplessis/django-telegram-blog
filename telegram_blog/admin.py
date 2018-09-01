from django.contrib import admin
from .models import Blog, Entry


class BlogAdmin(admin.ModelAdmin):
    pass


class EntryAdmin(admin.ModelAdmin):
    pass


admin.site.register(Blog, BlogAdmin)
admin.site.register(Entry, EntryAdmin)

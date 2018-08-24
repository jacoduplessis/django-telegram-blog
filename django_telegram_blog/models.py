# from django.contrib.postgres.fields import JSONField
import json

from django.core.files.storage import default_storage
from django.db import models
from django.utils.functional import cached_property
from django.conf import settings


class Blog(models.Model):
    time_created = models.DateTimeField(auto_now_add=True)
    telegram_chat_id = models.BigIntegerField()
    title = models.CharField(blank=True, max_length=300)

    def __str__(self):
        return self.title


class Entry(models.Model):

    TEXT = 'text'
    AUDIO = 'audio'
    DOCUMENT = 'document'
    VIDEO = 'video'
    ANIMATION = 'animation'
    PHOTO = 'photo'
    STICKER = 'sticker'
    VIDEO_NOTE = 'video_note'
    CONTACT = 'contact'
    LOCATION = 'location'
    VENUE = 'venue'

    TYPE_CHOICES = (
        (VIDEO, VIDEO),
        (PHOTO, PHOTO),
        (DOCUMENT, DOCUMENT),
        (AUDIO, AUDIO),
        (ANIMATION, ANIMATION),
        (STICKER, STICKER),
        (VIDEO_NOTE, VIDEO_NOTE),
        (CONTACT, CONTACT),
        (LOCATION, LOCATION),
        (VENUE, VENUE),
        (TEXT, TEXT),  # must be last
    )

    time_created = models.DateTimeField(auto_now_add=True)
    telegram_update_id = models.BigIntegerField()
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='entries')
    update = models.TextField()
    type = models.CharField(choices=TYPE_CHOICES, max_length=30, default=TEXT)
    message_time = models.DateTimeField()

    def __str__(self):
        return f'{self.blog_id} {self.telegram_update_id}'

    class Meta:
        verbose_name = 'Entry'
        verbose_name_plural = 'Entries'

    @cached_property
    def message(self):
        return json.loads(self.update).get('message')

    @cached_property
    def template(self):
        return f'telegram_blog/entry_{self.type}.html'

    def media_path(self, file_id):
        return f"{self.blog.telegram_chat_id}/{file_id}"

    def _save_media(self, file_id):
        from .telegram import get_telegram_file_content
        content = get_telegram_file_content(file_id)
        path = self.media_path(file_id)
        default_storage.save(path, content)

    @cached_property
    def photo_url(self):
        if self.type != Entry.PHOTO:
            return ''
        file_id = self.message['photo'][-1]['file_id']
        media_url = getattr(settings, 'MEDIA_URL')
        path = self.media_path(file_id)
        return media_url + path

    def save_media_files(self):
        if self.type == Entry.PHOTO:
            for photo_size in self.message['photo']:
                file_id = photo_size['file_id']
                self._save_media(file_id)
        if self.type == Entry.AUDIO:
            self._save_media(self.message['audio']['file_id'])
        if self.type == Entry.VIDEO:
            self._save_media(self.message['video']['file_id'])

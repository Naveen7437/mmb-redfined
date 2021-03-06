from unidecode import unidecode

from django.db import models
from django.dispatch import receiver
from django.utils.encoding import smart_text
from django.db.models.signals import post_save

from bands.models import Band
from mmb.settings import AUTH_USER_MODEL
from muse.app_settings import SONG_TAGS
from muse.utils import get_song_duration


def get_upload_file_name(instance, filename):
    """
    uploading songs
    """
    if not isinstance(filename, str):
        map(filename, str)

    filename = unidecode(smart_text(filename))

    if instance.band:
        id = instance.band.id
        name = 'band'
    else:
        id = instance.user.id
        name = 'user'

    return 'audio/{0}_{1}/{2}'.format(name, id, filename)


class Song(models.Model):
    # type = models.CharField(choices=SONG_TYPES, default='Audio')
    user = models.ForeignKey(AUTH_USER_MODEL, null=True, blank=True, default=None)
    band = models.ForeignKey(Band, null=True, blank=True, default=None)
    name = models.CharField(max_length=255)
    tags = models.CharField(choices=SONG_TAGS, max_length=255)
    likes = models.IntegerField(default=0)
    rating = models.IntegerField(default=3)
    upload = models.FileField(upload_to=get_upload_file_name)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    duration = models.CharField(max_length=15, blank=True, null=True)
    # singer = models.CharField(blank=True, max_length=255)
    # label = models.CharField(blank=True, max_length=255)
    # Todo: band song uploaded by

    def __str__(self):
        return '{}'.format(self.name)


@receiver(post_save, sender=Song)
def set_song_duration(sender, instance=None, created=False, **kwargs):
    if created:
        instance.duration = get_song_duration(instance.upload.path)
        instance.save()


class SongLike(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, null=True, blank=True, default=None)
    band = models.ForeignKey(Band, null=True, blank=True, default=None)
    song = models.ForeignKey(Song)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return '{} - {}'.format(self.user.username, self.song.name)


class PlayList(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(AUTH_USER_MODEL)
    song = models.ManyToManyField(Song, through="PlayListTrack")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} - {}'.format(self.name, self.user.username)


class PlayListTrack(models.Model):
    song = models.ForeignKey(Song)
    playlist = models.ForeignKey(PlayList)
    # order = models.IntegerField()

    # class Meta:
    #     ordering = ['order']

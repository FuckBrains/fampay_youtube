from django.db import models


class Videos(models.Model):
    video_id = models.CharField(max_length=100, blank=True, null=True)
    channel_id = models.CharField(max_length=100, blank=True, null=True)
    channel_title = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    publish_time = models.DateTimeField(blank=True, null=True)
    thumbnail_url_default = models.CharField(max_length=200, blank=True, null=True)
    thumbnail_url_medium = models.CharField(max_length=200, blank=True, null=True)
    thumbnail_url_high = models.CharField(max_length=200, blank=True, null=True)
    live_broadcast_content = models.CharField(max_length=200, blank=True, null=True)
    query_name = models.CharField(max_length=100, blank=True, null=True)
    query_type = models.CharField(max_length=100, blank=True, null=True)
    published_after = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'videos'

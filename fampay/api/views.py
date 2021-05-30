from api.models import Videos
from django.core import serializers
from django.http import HttpResponse


def youtube_list(request, max_results):
    youtube_videos_data = []
    youtube_videos_objects = Videos.objects.order_by('-id')[:max_results]
    for youtube_videos_object in youtube_videos_objects:
        youtube_videos_data_dict = {
            "video_id": youtube_videos_object.video_id,
            "channel_id": youtube_videos_object.channel_id,
            "channel_title": youtube_videos_object.channel_title,
            "title": youtube_videos_object.title,
            "description": youtube_videos_object.description,
            "publish_time": youtube_videos_object.publish_time,
            "thumbnail_url_default": youtube_videos_object.thumbnail_url_default,
            "thumbnail_url_medium": youtube_videos_object.thumbnail_url_medium,
            "thumbnail_url_high": youtube_videos_object.thumbnail_url_high,
            "live_broadcast_content": youtube_videos_object.live_broadcast_content,
            "query_name": youtube_videos_object.query_name,
            "query_type": youtube_videos_object.query_type,
            "published_after": youtube_videos_object.published_after,
            "created_at": youtube_videos_object.created_at
        }

        youtube_videos_data.append(youtube_videos_data_dict)

    return HttpResponse(youtube_videos_data)

from api.models import Videos
from django.core import serializers
from django.http import HttpResponse


def youtube_list(request, max_results):
    youtube_videos_objects = Videos.objects.order_by('-id')[:max_results]
    youtube_videos_data = serializers.serialize('json', youtube_videos_objects)

    return HttpResponse(youtube_videos_data)

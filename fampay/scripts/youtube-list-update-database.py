import os
import sys
from datetime import datetime

import django
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse
from googleapiclient.discovery import build

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../fampay')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
django.setup()

from api.models import Videos

DEVELOPER_KEY = 'AIzaSyC1Co1nfjY2fY5xXyEx3J5d0Q7_j2CtRaQ'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'


class YoutubeFamPay:
    def __init__(self, q):
        self.current_datetime = datetime.utcnow() - relativedelta(minutes=330)
        self.youtube = build(
            YOUTUBE_API_SERVICE_NAME,
            YOUTUBE_API_VERSION,
            developerKey=DEVELOPER_KEY
        )
        self.q = q

        self.youtube_search_data = []

    def execute(self):
        self._get_youtube_list_data()
        self._insert_in_db()

    def _get_youtube_list_data(self):
        # query term | published in 1 month
        list_q = self.q
        list_type = "video"
        list_order = "date"
        list_published_after = datetime.strftime(
            self.current_datetime - relativedelta(months=1),
            '%Y-%m-%dT%H:%M:%SZ'
        )

        # Call the search.list method to retrieve results matching the specified
        search_response = self.youtube.search().list(
            q=list_q,
            part="id,snippet",
            type=list_type,
            order=list_order,
            publishedAfter=list_published_after
        ).execute()

        items = search_response.get("items", [])
        for item in items:
            if item['id']['kind'] != 'youtube#video':
                continue

            self.youtube_search_data.append(
                {
                    "video_id": item["id"]["videoId"],
                    "channel_id": item["snippet"]["channelId"],
                    "channel_title": item["snippet"]["channelTitle"],
                    "title": item["snippet"]["title"],
                    "description": item["snippet"]["description"],
                    "publish_time": parse(str(item["snippet"]["publishTime"])),
                    "thumbnail_url_default": item["snippet"]["thumbnails"]['default']['url'],
                    "thumbnail_url_medium": item["snippet"]["thumbnails"]['medium']['url'],
                    "thumbnail_url_high": item["snippet"]["thumbnails"]['high']['url'],
                    "live_broadcast_content": item["snippet"]["liveBroadcastContent"],
                    "query_q": list_q,
                    "query_type": list_type,
                    "published_after": parse(str(list_published_after))
                }
            )

    def _insert_in_db(self):
        if not self.youtube_search_data:
            return

        print("inserting data in db...")

        for youtube_data in self.youtube_search_data:
            print("...inserting in db: ", youtube_data.get('video_id'))
            Videos.objects.get_or_create(
                video_id=youtube_data.get('video_id'),
                channel_id=youtube_data.get('channel_id'),
                channel_title=youtube_data.get('channel_title'),
                title=youtube_data.get('title'),
                description=youtube_data.get('description'),
                publish_time=youtube_data.get('publish_time'),
                thumbnail_url_default=youtube_data.get('thumbnail_url_default'),
                thumbnail_url_medium=youtube_data.get('thumbnail_url_medium'),
                thumbnail_url_high=youtube_data.get('thumbnail_url_high'),
                live_broadcast_content=youtube_data.get('live_broadcast_content'),
                query_name=youtube_data.get('query_q'),
                query_type=youtube_data.get('query_type'),
                published_after=youtube_data.get('published_after'),
                created_at=self.current_datetime
            )


if __name__ == "__main__":
    try:
        query = "official"
        youtube_fam_pay_object = YoutubeFamPay(q=query)
        youtube_fam_pay_object.execute()
    except Exception as err:
        print(err)

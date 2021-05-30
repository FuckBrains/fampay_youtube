from django.urls import path
from api import views

urlpatterns = [
    path("youtube/list/<int:max_results>", views.youtube_list, name='list'),
]

# urls.py
# urls.py

from django.urls import path, re_path
from . import views
from .consumers import VideoStreamConsumer

websocket_urlpatterns = [
    re_path(r'ws/video_stream/$', VideoStreamConsumer.as_asgi()),
]

urlpatterns = [
    path('video_stream/', views.video_stream_view, name='video_stream'),
]

urlpatterns += websocket_urlpatterns
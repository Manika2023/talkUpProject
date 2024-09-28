# routing.py

from django.urls import re_path
from masterBoard import consumers

websocket_urlpatterns = [
    re_path(r'ws/masterboard/$', consumers.MasterBoardConsumer.as_asgi()),
]
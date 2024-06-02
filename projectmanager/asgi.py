"""
ASGI config for projectmanager project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path
from volume_control.consumers import VideoStreamConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projectmanager.settings')
django.setup()

# ws_pattern = [
#     path('ws/video_stream/', VideoStreamConsumer.as_asgi()),
# ]

# application = ProtocolTypeRouter({
#     'http': get_asgi_application(),
#     'websocket': URLRouter(ws_pattern),
# })

django.setup()

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': URLRouter([]),
})
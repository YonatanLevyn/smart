"""
ASGI config for site_proj project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

# site_proj/asgi.py

import os
from django.core.asgi import get_asgi_application
from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from analytics import consumers

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'site_proj.settings')

application = ProtocolTypeRouter(
    {
        'http': get_asgi_application(),
        'websocket': AuthMiddlewareStack(
            URLRouter(
                [
                    path('ws/analytics/', consumers.AnalyticsConsumer.as_asgi()),
                ]
            )
        ),
    }
)

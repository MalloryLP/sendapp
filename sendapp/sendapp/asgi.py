"""
WSGI config for sendapp project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os, django

from django.core.asgi import get_asgi_application

django_asgi_app = get_asgi_application()

from channels.auth import AuthMiddlewareStack

from channels.routing import ProtocolTypeRouter, URLRouter

from chat.routing import ws_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sendapp.settings')
django.setup()

application = ProtocolTypeRouter({
  'https': django_asgi_app,
  'websocket': AuthMiddlewareStack(URLRouter(ws_urlpatterns))
})


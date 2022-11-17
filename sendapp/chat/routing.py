from importlib.resources import path
from django.urls import path

from chat.consumers import PersonalChatConsumer

ws_urlpatterns = {
    path('ws/<int:id>/', PersonalChatConsumer.as_asgi())
}
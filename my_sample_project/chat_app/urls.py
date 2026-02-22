from django.urls import path
from . import views

urlpatterns = [
    path('chat/room/<int:topic_id>', views.chat_room, name='chat_room'),
]

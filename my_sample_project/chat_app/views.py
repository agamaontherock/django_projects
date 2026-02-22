from django.shortcuts import render
from .models import Topic
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def chat_room(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    last_messages = topic.message_set.all().order_by('-sent_on')[:5]
    last_messages = reversed(last_messages)
    return render(request, 'chat_app/chat_room.html', {'topic': topic, 'last_message': last_messages})
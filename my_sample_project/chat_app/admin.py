from django.contrib import admin

from .models import Topic, Message
# Register your models here.
admin.site.register(Topic)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sent_on', 'user', 'topic', 'message']
    list_filter = ['sent_on', 'topic']
    search_fields = ['message']
    # raw_id_fields = ['user', 'message']
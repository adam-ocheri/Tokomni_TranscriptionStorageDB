from rest_framework import serializers
from .models import ConversationItem

class ConversationItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversationItem
        fields = ['text', 'speaker', 'search_vector', 'timestamp', 'call_part']
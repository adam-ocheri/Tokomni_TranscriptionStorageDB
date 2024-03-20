from rest_framework import serializers
from .models import ConversationItem, CallPart

class ConversationItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversationItem
        fields = ['text', 'speaker', 'search_vector', 'timestamp', 'call_part']
        extra_kwargs = {
            'speaker': {'required': False},
            'call_part': {'required': False},
            'timestamp': {'required': False}
        }

class CallPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallPart
        fields = ['callog_uuid', 'file_location']
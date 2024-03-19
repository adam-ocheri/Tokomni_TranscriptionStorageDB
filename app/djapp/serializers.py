from rest_framework import serializers
from .models import ConversationItem, CallPart

class ConversationItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversationItem
        fields = ['text', 'speaker', 'search_vector', 'timestamp', 'call_part']

class CallPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallPart
        fields = ['text', 'speaker', 'search_vector', 'timestamp', 'call_part']
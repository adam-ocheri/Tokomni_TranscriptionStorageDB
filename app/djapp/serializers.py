from rest_framework import serializers
from .models import ConversationItem, CallPart, FullCallData

class ConversationItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversationItem
        fields = ['text', 'speaker', 'search_vector', 'timestamp', 'call_part']
        extra_kwargs = {
            'speaker': {'required': False},
            'callpart_id': {'required': False},
            'timestamp': {'required': False}
        }

class CallPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallPart
        fields = ['fullcall_id', 'file_location', 'extension']

class FullCallDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FullCallData
        fields = ['cdr_uuid']
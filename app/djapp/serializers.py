from rest_framework import serializers
from .models import ConversationItem, CallPart, FullCallData

class ConversationItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversationItem
        fields = "__all__"
        extra_kwargs = {
            'speaker': {'required': False},
            'callpart_id': {'required': False},
            'timestamp': {'required': False},
            # 'id': {'editable': False}
        }

class CallPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallPart
        fields = "__all__"

class FullCallDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FullCallData
        fields = "__all__"
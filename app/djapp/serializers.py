from rest_framework import serializers
from .models import ConversationItem, CallPart, FullCallData
import uuid

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
    # def validate_id(self, value):
    #     """
    #     Validate that the UUID is in the correct format.
    #     """
    #     try:
    #         uuid.UUID(value, version=4)
    #     except ValueError:
    #         raise serializers.ValidationError("This is not a valid UUID.")
    #     return value

class CallPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallPart
        fields = "__all__"

    # def validate_id(self, value):
    #     """
    #     Validate that the UUID is in the correct format.
    #     """
    #     try:
    #         uuid.UUID(value, version=4)
    #     except ValueError:
    #         raise serializers.ValidationError("This is not a valid UUID.")
    #     return value

class FullCallDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FullCallData
        fields = "__all__"
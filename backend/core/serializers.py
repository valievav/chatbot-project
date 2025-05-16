from rest_framework import serializers
from core.models import AiChatSession


class AiChatSessionMessageSerializer(serializers.Serializer):
    role = serializers.CharField()
    parts = serializers.CharField()


class AiChatSessionSerializer(serializers.ModelSerializer):
    """
    Serializer for AiChatSession
    """
    messages = AiChatSessionMessageSerializer(many=True)

    def to_representation(self, instance):
        """
        Convert the instance to a dictionary representation
        """
        representation = super().to_representation(instance)
        representation['messages'] = [msg for msg in representation['messages']
                                      if msg['role'] != 'system']
        return representation

    class Meta:
        model = AiChatSession
        fields = ['id', 'messages']
        read_only_fields = ['messages']

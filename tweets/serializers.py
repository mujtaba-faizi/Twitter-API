from rest_framework import serializers
from .models import Tweet


class TweetSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Tweet
        fields = ['id', 'text', 'owner', 'created_at', 'updated_at']

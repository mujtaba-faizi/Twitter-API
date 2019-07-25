from rest_framework import serializers
from django.contrib.auth.models import User
from tweets.models import Tweet


class UserSerializer(serializers.ModelSerializer):
    tweets = serializers.PrimaryKeyRelatedField(many=True, queryset=Tweet.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'tweets']


class TweetSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Tweet
        fields = ['id', 'text', 'owner', 'created_at', 'updated_at']


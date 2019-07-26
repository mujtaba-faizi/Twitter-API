from rest_framework import serializers
from django.contrib.auth.models import User
from tweets.models import Tweet
from .models import Follower


class UserSerializer(serializers.ModelSerializer):
    tweets = serializers.PrimaryKeyRelatedField(many=True, queryset=Tweet.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'tweets']


class FollowerSerializer(serializers.ModelSerializer):
    tweets = serializers.PrimaryKeyRelatedField(many=True, queryset=Tweet.objects.all())

    class Meta:
        model = Follower
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'tweets']





from rest_framework import serializers
from django.contrib.auth.models import User
from tweets.models import Tweet
from .models import Follower


class UserSerializer(serializers.ModelSerializer):
    # tweets = serializers.PrimaryKeyRelatedField(many=True, queryset=Tweet.objects.all())
    followed_by = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'tweets', 'followed_by']


class FollowerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follower
        fields = ['follower_user', 'followee_user']





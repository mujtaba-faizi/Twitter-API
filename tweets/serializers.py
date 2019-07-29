from rest_framework import serializers
from .models import Tweet, Comment, Like


class TweetSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    likes = serializers.IntegerField(source='count')
    liked_by = serializers.StringRelatedField(many=True, read_only=True)
    comments = serializers.PrimaryKeyRelatedField(many=True, queryset=Comment.objects.all())

    class Meta:
        model = Tweet
        fields = ['id', 'text', 'owner', 'created_at', 'updated_at', 'likes', 'liked_by', 'comments']


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Comment
        fields = ['id', 'text', 'owner', 'tweet']


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ['id', 'user', 'tweet']

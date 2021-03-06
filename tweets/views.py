from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import Tweet, Comment, Like
from django.contrib.auth.models import User
from .serializers import TweetSerializer, LikeSerializer, CommentSerializer
from rest_framework import permissions, viewsets, status
from users.permissions import IsOwnerOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response


class InputTweet(generic.DetailView):
    model = User
    template_name = 'tweets/tweet.html'


def show_profile(request, user_id, profile_id):
    user = User.objects.get(id=profile_id)
    context = {
        'user': user,
        'user_id': user_id,
    }
    return render(request, 'tweets/profile.html', context)


def save_tweet(request, user_id):
    new_tweet = Tweet()
    new_tweet.user_id = user_id
    new_tweet.text = request.POST['tweet']
    new_tweet.save()
    return HttpResponseRedirect(reverse('users:user_home', args=(user_id,)))


def show_users(request, follower_user_id):
    users = User.objects.all()
    context = {
        'users': users,
        'follower_user_id': follower_user_id,
    }
    return render(request, 'tweets/users.html', context)


def like(request, user_id, profile_id, tweet_id, page):
    try:
        Like.objects.get(tweet_id=tweet_id, user_id=user_id)
    except (KeyError, Like.DoesNotExist):
        like = Like()
        like.tweet_id = tweet_id
        like.user_id = user_id
        like.save()
    if page == 'user_home':
        return HttpResponseRedirect(reverse('users:user_home', args=(user_id,)))
    elif page == 'profile':
        return HttpResponseRedirect(reverse('tweets:user_profile', args=(user_id, profile_id)))


def show_likes(request, user_id, tweet_id):
    likes = Like.objects.filter(tweet_id=tweet_id)
    context = {
        'user_id': user_id,
        'likes': likes,
    }
    return render(request, 'tweets/likes.html', context)


def comment(request, user_id, profile_id, tweet_id, page):
    context = {
        'user_id': user_id,
        'profile_id': profile_id,
        'tweet_id': tweet_id,
        'page': page
    }
    return render(request, 'tweets/comment_form.html', context)


def save_comment(request, user_id, profile_id, tweet_id, page):
    comment = Comment()
    comment.text = request.POST['comment']
    comment.tweet_id = tweet_id
    comment.user_id = user_id
    comment.save()
    if page == 'user_home':
        return HttpResponseRedirect(reverse('users:user_home', args=(user_id,)))
    elif page == 'profile':
        return HttpResponseRedirect(reverse('tweets:user_profile', args=(user_id, profile_id)))


def show_comments(request, user_id, tweet_id):
    tweet = Tweet.objects.get(id=tweet_id)
    context = {
        'user_id': user_id,
        'tweet': tweet,
    }
    return render(request, 'tweets/comments.html', context)


class TweetViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LikeTweet(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def post(self, request, pk, format=None):
        try:
            Like.objects.get(tweet_id=pk, user_id=request.user.id)
            return Response({"detail": "Already liked !!"}, status=status.HTTP_208_ALREADY_REPORTED)
        except (KeyError, Like.DoesNotExist):  # If the user is not already liked
            mutable = request.POST._mutable
            request.POST._mutable = True  # to solve the issue of QueryDict instance being immutable
            request.POST['user'] = request.user.id
            request.POST['tweet'] = pk
            request.POST._mutable = mutable
            serializer = LikeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            like_object = Like.objects.get(tweet_id=pk, user_id=request.user.id)
            like_object.delete()
            return Response({"detail": "Succesfully unliked !!"}, status=status.HTTP_204_NO_CONTENT)
        except (KeyError, Like.DoesNotExist):  # If the user is not already followed
            return Response({"detail": "Not liked"}, status=status.HTTP_400_BAD_REQUEST)


class CommentTweet(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def post(self, request, pk, format=None):
        mutable = request.POST._mutable
        request.POST._mutable = True         # to solve the issue of QueryDict instance being immutable
        request.POST['tweet'] = pk
        request.POST._mutable = mutable
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

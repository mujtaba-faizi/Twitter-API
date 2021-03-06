from django.http import HttpResponse, HttpResponseRedirect, Http404
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import Follower
# from .models import User
from tweets.models import Tweet
from django.contrib.auth.models import User
from .serializers import UserSerializer, FollowerSerializer
from rest_framework import permissions, viewsets, status
from users.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import action
from rest_framework.views import APIView


class HomeView(generic.TemplateView):
    template_name = 'users/home.html'


class SignUp(generic.TemplateView):
    template_name = 'users/signup.html'


class SignIn(generic.TemplateView):
    template_name = 'users/signin.html'


class SignOut(generic.TemplateView):
    template_name = 'users/home.html'


class Update(generic.DetailView):
    model = User
    template_name = 'users/update_form.html'


def show_homepage(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        tweets = Tweet.objects.all()
    except User.DoesNotExist:
        raise Http404("User does not exist")
    return render(request, 'users/user_home.html', {'user': user, 'tweets': tweets})


def save_user(request):
    new_user = User()
    new_user.email = request.POST['email']
    new_user.password = request.POST['pass']
    new_user.first_name = request.POST['f_name']
    new_user.last_name = request.POST['l_name']
    new_user.username = request.POST['username']
    new_user.phone = request.POST['no']
    new_user.save()
    return HttpResponseRedirect(reverse('users:signin'))


def authenticate(request):
    username = request.POST['username']
    password = request.POST['pass']
    user = get_object_or_404(User, username=username, password=password)
    return HttpResponseRedirect(reverse('users:user_home', args=(user.id,)))


def update_profile(request, user_id):
    try:
        email = request.POST['email']
        password = request.POST['pass']
        first_name = request.POST['f_name']
        last_name = request.POST['l_name']
        phone = request.POST['no']
        user = User.objects.filter(id=user_id).update(email=email, password=password, first_name=first_name,
                                                      last_name=last_name, phone=phone)
    except User.DoesNotExist:
        raise Http404("User does not exist")
    return HttpResponseRedirect(reverse('users:user_home', args=(user_id,)))


def add_follower(request, follower_user_id, followee_user_id):
    try:
        Follower.objects.get(followee_user_id=followee_user_id, follower_user_id=follower_user_id)
    except (KeyError, Follower.DoesNotExist):       # If the user is not already followed
        new_follower = Follower()
        new_follower.follower_user_id = follower_user_id
        new_follower.followee_user_id = followee_user_id
        user = User.objects.get(pk=followee_user_id)
        new_follower.followee_name = user.username
        new_follower.save()
    return HttpResponseRedirect(reverse('tweets:show_all_users', args=(follower_user_id,)))


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def update(self, request, *args, **kwargs):
        """
        Update user profile
        """
        if int(kwargs['pk']) is not request.user.id:
            return Response({"detail": "User is not authorized"}, status=status.HTTP_401_UNAUTHORIZED)
        return super(UserViewSet, self).update(request, *args, **kwargs)


class FollowUser(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def post(self, request, pk, format=None):
        if pk is request.user.id:
            return Response({"detail": "You cannot follow yourself"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            Follower.objects.get(follower_user_id=pk, followee_user_id=request.user.id)
            return Response({"detail": "Already followed !!"}, status=status.HTTP_208_ALREADY_REPORTED)
        except (KeyError, Follower.DoesNotExist):  # If the user is not already followed
            data = request.data
            data['follower_user'] = pk
            data['followee_user'] = request.user.id
            serializer = FollowerSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            follow_object = Follower.objects.get(follower_user_id=pk, followee_user_id=request.user.id)
            follow_object.delete()
            return Response({"detail": "Succesfully unfollowed !!"}, status=status.HTTP_204_NO_CONTENT)
        except (KeyError, Follower.DoesNotExist):  # If the user is not already followed
            return Response({"detail": "Not followed"}, status=status.HTTP_400_BAD_REQUEST)

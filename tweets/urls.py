from django.urls import path, include
from tweets import views
from rest_framework.routers import DefaultRouter


app_name = "tweets"

router = DefaultRouter()
router.register(r'tweets', views.TweetViewSet)
router.register(r'comments', views.CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('tweets/<int:pk>/like/', views.LikeTweet.as_view()),
    path('tweets/<int:pk>/comment/', views.CommentTweet.as_view()),

    path('<int:user_id>/save/', views.save_tweet, name='save_tweet'),
    path('<int:pk>/tweetform/', views.InputTweet.as_view(), name='tweet_form'),
    path('<int:follower_user_id>/users/', views.show_users, name='show_all_users'),
    path('<int:user_id>/<int:profile_id>/profile/', views.show_profile, name='user_profile'),
    path('<int:user_id>/<int:profile_id>/<int:tweet_id>/<str:page>/like/', views.like, name='like'),
    path('<int:user_id>/<int:profile_id>/<int:tweet_id>/<str:page>/comment/', views.comment, name='comment_form'),
    path('<int:user_id>/<int:profile_id>/<int:tweet_id>/<str:page>/save_comment/', views.save_comment, name='comment'),
    path('<int:user_id>/<int:tweet_id>/comments/', views.show_comments, name='show_comments'),
    path('<int:user_id>/<int:tweet_id>/likes/', views.show_likes, name='show_likes'),
]

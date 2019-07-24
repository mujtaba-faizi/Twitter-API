from django.urls import path, include, re_path
from users import views as views
from rest_auth.registration.views import VerifyEmailView, RegisterView


app_name = "users"
urlpatterns = [
    path('auth/', include('rest_auth.urls')),
    path('auth/signup/', include('rest_auth.registration.urls')),
    path('registration/', RegisterView.as_view(), name='account_signup'),
    re_path(r'^account-confirm-email/', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$', VerifyEmailView.as_view(), name='account_confirm_email'),
    path('home/', views.HomeView.as_view(), name='home'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('signup/save/', views.save_user, name='save_user'),
    path('signup/authenticate/', views.authenticate, name='authenticate'),
    path('<int:user_id>/', views.show_homepage, name='user_home'),
    path('<int:pk>/updateform/', views.Update.as_view(), name='update_form'),
    path('<int:user_id>/update/', views.update_profile, name='update'),
    path('signin/', views.SignIn.as_view(), name='signin'),
    path('<int:follower_user_id>/users/<int:followee_user_id>/follow/', views.add_follower, name='add_follower'),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('tweets/', views.TweetList.as_view()),
    path('tweets/<int:pk>', views.TweetDetail.as_view()),

]

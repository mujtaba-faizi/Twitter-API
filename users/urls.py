from django.urls import path, include
from users import views as views
from rest_framework.routers import DefaultRouter


app_name = "users"

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'users', views.UserViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_auth.urls')),
    path('auth/signup/', include('rest_auth.registration.urls')),
    path('home/', views.HomeView.as_view(), name='home'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('signup/save/', views.save_user, name='save_user'),
    path('signup/authenticate/', views.authenticate, name='authenticate'),
    path('<int:user_id>/', views.show_homepage, name='user_home'),
    path('<int:pk>/updateform/', views.Update.as_view(), name='update_form'),
    path('<int:user_id>/update/', views.update_profile, name='update'),
    path('signin/', views.SignIn.as_view(), name='signin'),
    path('<int:follower_user_id>/users/<int:followee_user_id>/follow/', views.add_follower, name='add_follower'),

]


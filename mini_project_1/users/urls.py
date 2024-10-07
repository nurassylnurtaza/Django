from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import user_register, profile_view, edit_profile, follow_user, unfollow_user, user_list, CustomLoginView, \
    home_view, logout_view

urlpatterns = [
    path('', home_view, name='home'),
    path('login', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('list', user_list, name='user_list'),
    path('register/', user_register, name='register'),
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('profile/<str:username>/', profile_view, name='profile'),
    path('follow/<str:username>/', follow_user, name='follow_user'),
    path('unfollow/<str:username>/', unfollow_user, name='unfollow_user'),
]

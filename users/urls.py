from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    # path('', views.users_detail),
    path('signup/auth/', views.users_signup_auth, name='signup_auth'),
    path('signup/', views.users_signup, name='signup'),
    path('signin/', views.users_signin, name='signin'),
    path('password/auth/', views.users_password_auth, name='password_auth'),
    path('password/', views.users_password, name='password'),
    # path('', views.users_list, name=''),
]
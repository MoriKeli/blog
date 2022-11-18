from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserLogin.as_view(), name='login'),
    path('create-account/', views.signup_view, name='signup'),
    path('profile/', views.userprofile_view, name='profile'),
    path('homepage/', views.homepage_view, name='homepage'),
    path('blog/', views.blogging_view, name='upload_blog'),
    path('logout/', views.LogoutUser.as_view(), name='user_logout'),

]
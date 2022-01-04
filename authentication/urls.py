# Here we write all the links connected in our app and we don't need to add them in main urls(loginsystem), because we pass link of this url already...

from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from . import views

urlpatterns = [
      path('',views.home,  name="home"),
      path('signin/',views.signin,  name="signin"),
      path('signup/',views.signup,  name="signup"),
      path('signout/',views.signout,  name="signout"),
      path('activate/<uidb64>/<token>',views.activate,  name="activate"),
    #   path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',views.activate, name='activate'),  
]
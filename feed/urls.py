from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('pusher_authentication', views.pusher_authentication, name = 'pusher_authentication'),
    path('push_feed', views.push_feed, name = 'push_feed'),

]


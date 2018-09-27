from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^welcome$', views.welcome),
    url(r'^user_profile$', views.user_profile),
    url(r'^belt_details$', views.belt_details),
    url(r'^destroy/(?P<id>\d+)$', views.destroy)
]
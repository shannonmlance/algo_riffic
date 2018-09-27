from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^level_assessment/(?P<number>\d+)$', views.level_assessment),
    url(r'^level_assessment/(?P<number>\d+)/compare_answer$', views.level_assessment_compare_answer),
    url(r'^level_assessment/evaluation$', views.level_assessment_evaluation)
]
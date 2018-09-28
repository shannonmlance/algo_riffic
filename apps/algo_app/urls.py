from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^level_assessment/(?P<lnum>\d+)$', views.level_assessment),
    url(r'^level_assessment/(?P<lnum>\d+)/compare_answer$', views.level_assessment_compare_answer),
    url(r'^level_assessment/evaluation$', views.level_assessment_evaluation),
    url(r'^level_practice/(?P<lnum>\d+)/(?P<slnum>\d+)$', views.level_practice),
    url(r'^level_practice/(?P<lnum>\d+)/(?P<slnum>\d+)/compare_answer$', views.level_practice_compare_answer)
]
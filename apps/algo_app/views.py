from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from apps.login_app.models import User
from .models import *
import bcrypt
from time import localtime, strftime
import re

# called by "/level_assessment/<number>" through "url(r'^level_assessment/(?P<number>\d+)$', views.level_assessment)"
def level_assessment(request, number):
    # if page was accessed through login app
    if "id" in request.session:
        # add algorithms to context
        context = {
            "lesson" : Lesson.objects.get(number=number),
            "user" : User.objects.get(id=request.session["id"])
        }
        # render template
        return render(request, "algo_app/level_assessment.html", context)
    # otherwise
    else:
        # redirect to login app
        return redirect("/")

# called by "/level_assessment/<number>/compare_answer" through url(r'^level_assessment/(?P<number>\d+)/compare_answer$', views.level_assessment_compare_answer)
def level_assessment_compare_answer(request, number):
    # if page was accessed through POST
    if request.method == "POST":
        # compare POSTed information with database answer
        answer_correct = True
        this_lesson = Lesson.objects.get(number=number)
        answers = this_lesson.answers.all()
        answer_regex = re.compile(answers[0].regex)
        if answer_regex.match(request.POST["answer1"]):
            print("my regex worked!!!!")
            # return boolean
            # redirect to evaluation page
            return redirect("/level_assessment/evaluation")
        else:
            print("my regex failed")
            return redirect("/level_assessment/evaluation")
    # otherwise
    else:
        # redirect to login app
        return redirect("/")

# called by "/level_assessment/evaluation" through url(r'^level_assessment/evaluation$', views.level_assessment_evaluation)
def level_assessment_evaluation(request):
    # if page was accessed through login app
    if "id" in request.session:
        # if boolean == True
            # update dojo point += 50
            # increase level
        # otherwise
            # increase sublevel
        # render evaluation page
        return render(request, "algo_app/level_assessment_evaluation.html")
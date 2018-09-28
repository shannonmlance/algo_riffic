from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from apps.login_app.models import User
from .models import *
import bcrypt
from time import localtime, strftime
import re

# called by "/level_assessment/<lnum>" through "url(r'^level_assessment/(?P<lnum>\d+)$', views.level_assessment)"
def level_assessment(request, lnum):
    # if page was accessed through login app
    if "id" in request.session:
        # add algorithms to context
        this_lesson = Lesson.objects.get(number=lnum)
        context = {
            "lesson" : this_lesson,
            "user" : User.objects.get(id=request.session["id"]),
            "questions" : this_lesson.questions.all()
        }
        # render template
        return render(request, "algo_app/level_assessment.html", context)
    # otherwise
    else:
        # redirect to login app
        return redirect("/")

# called by "/level_assessment/<lnum>/compare_answer" through url(r'^level_assessment/(?P<lnum>\d+)/compare_answer$', views.level_assessment_compare_answer)
def level_assessment_compare_answer(request, lnum):
    # if page was accessed through POST
    if request.method == "POST":
        # set all the variables
        if "answer_correct" not in request.session:
            request.session["answer_correct"] = True
        request.session["answer_correct"] = True
        this_user = User.objects.get(id=request.session["id"])
        this_lesson = Lesson.objects.get(number=lnum)
        answers = this_lesson.answers.all()
        post_answers = []
        # iterate through the POST to get the answers for comparison
        for k in request.POST:
            if k != "csrfmiddlewaretoken":
                for x in request.POST.getlist(k):
                    post_answers.append(x)
        # compare the POSTed information with the database answer
        for i in range(len(post_answers)):
            answer_regex = re.compile(answers[i].regex)
            # if one of the answers is wrong, update the user information
            if not answer_regex.match(post_answers[i]):
                request.session["answer_correct"] = False
                this_user.current_sub_lesson += 1
                this_user.save()
                return redirect("/level_assessment/evaluation")
        # if all of the answers are correct, update the user information
        this_user.dojo_points += 50
        this_user.belt_rank += 1
        this_user.current_lesson += 1
        this_user.current_sub_lesson = 0
        this_user.save()
        # redirect to evaluation page
        return redirect("/level_assessment/evaluation")
    # otherwise
    else:
        # redirect to login app
        return redirect("/")

# called by "/level_assessment/evaluation" through url(r'^level_assessment/evaluation$', views.level_assessment_evaluation)
def level_assessment_evaluation(request):
    # if page was accessed through login app
    if "id" in request.session:
        context = {
            "user" : User.objects.get(id=request.session["id"])
        }
        # render evaluation page
        return render(request, "algo_app/level_assessment_evaluation.html", context)

# called by "/level_practice/<lnum>/<slnum>" through url(r'^level_practice/(?P<lnum>\d+)/(?P<slnum>\d+)$', views.level_practice)
def level_practice(request, lnum, slnum):
    # if page was accessed through login app
    if "id" in request.session:
        this_lesson = Lesson.objects.get(number=lnum)
        sub_lessons = Sub_lesson.objects.filter(lessons=this_lesson)
        this_sub_lesson = sub_lessons.get(number=slnum)
        this_user = User.objects.get(id=request.session["id"])
        context = {
            "user" : this_user,
            "sub_lesson" : this_sub_lesson,
            "questions" : this_sub_lesson.questions.all(),
            "lesson" : this_lesson
        }
        # depending on the sub_lesson number, render the appropriate practice page
        if this_sub_lesson.number == 1:
            print("going to drag-and-drop pseudocode")
            return render(request, "algo_app/drag-and-drop/pseudocode.html", context)
        if this_sub_lesson.number == 2:
            print("going to drag-and-drop code")
            return render(request, "algo_app/drag-and-drop/code.html", context)
        if this_sub_lesson.number == 3:
            print("going to fill-in-the-blank")
            return render(request, "algo_app/fill-in-the-blank.html", context)
        if this_sub_lesson.number == 4:
            print("going to code-prediction")
            return render(request, "algo_app/code-prediction.html", context)
        else:
            this_user.current_lesson += 1
            this_user.current_sub_lesson = 0
            this_user.save()
            return redirect("/level_assessment/"+str(this_user.current_lesson))
    else:
        return redirect("/")

# called by "/level+practice/<lnum>/<slnum>/compare_answer" through url(r'^level_practice/(?P<lnum>\d+)/(?P<slnum>\d+)/compare_answer$', views.level_practice_compare_answer)
def level_practice_compare_answer(request, lnum, slnum):
    # if page was accessed through POST
    if request.method == "POST":
        # set all the variables
        request.session["answer_correct"] = True
        this_user = User.objects.get(id=request.session["id"])
        this_lesson = Lesson.objects.get(number=lnum)
        sub_lessons = Sub_lesson.objects.filter(lessons=this_lesson)
        this_sub_lesson = sub_lessons.get(number=slnum)
        answers = this_sub_lesson.answers.all()
        post_answers = []
        # iterate through the POST to get the answers for comparison
        print("this is the POST:", request.POST)
        for k in request.POST:
            print("this is the key from the POST:", k)
            if k != "csrfmiddlewaretoken":
                print("this is the key that passed the if statement:", k)
                for x in request.POST.getlist(k):
                    print("this is the key, value pair:", k, x)
                    post_answers.append(x)
                    print("this is the list of answers:", post_answers)
        # compare the POSTed information with the database answer
        for i in range(len(post_answers)):
            answer_regex = re.compile(answers[i].regex)
            # if one of the answers is wrong, update the user information
            if not answer_regex.match(post_answers[i]):
                request.session["answer_correct"] = False
                messages.error(request, "That answer is not correct. Try again.")
                return redirect("/level_practice/"+str(this_lesson.number)+"/"+str(this_sub_lesson.number))
        # if all of the answers are correct, update the user information
        this_user.dojo_points += 10
        this_user.current_sub_lesson += 1
        this_user.save()
        print(this_user.current_lesson, this_user.current_sub_lesson)
        # redirect to evaluation page
        return redirect("/level_practice/"+str(this_user.current_lesson)+"/"+str(this_user.current_sub_lesson))
    # otherwise
    else:
        # redirect to login app
        return redirect("/")

# called by "sub_lesson/drag_and_drop/pseudo_code" through url(r'^sub_lesson/drag_and_drop/pseudo_code$', views.sub_lesson_drag_and_drop_pseudo_code)
def sub_lesson_drag_and_drop_pseudo_code(request):
    if "id" in request.session:
        return render(request, "algo_app/pseudo_code_level.html")
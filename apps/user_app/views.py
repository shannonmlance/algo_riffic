from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from apps.login_app.models import User
import bcrypt
from time import localtime, strftime

# called by "/welcome" through url(r'^welcome$', views.welcome)
def welcome(request):
    # if the page is accessed through the dashboard
    if "id" in request.session:
        # set logged_in as true
        request.session["logged_in"] = True
        # render welcome page
        return render(request, "user_app/welcome.html")
    # otherwise
    else:
        # redirect to login page
        return redirect("/")

# called by "/user_profile" through url(r'^user_profile$', views.user_profile)
def user_profile(request):
    # if the page is accessed through the dashboard
    if "id" in request.session:
        # put user into context
        context = {
            "user" : User.objects.get(id=request.session["id"])
        }
        # render user_profile page
        return render(request, "user_app/user_profile.html", context)
    # otherwise
    else:
        # redirect to login page
        return redirect("/")

# called by "/belt_details" through url(r'^belt_details$', views.belt_details)
def belt_details(request):
    # if the page is accessed through the dashboard
    if "id" in request.session:
        # set logged_in as true
        request.session["logged_in"] = True
        # render belt_details page
        return render(request, "user_app/belt_details.html")
    # otherwise
    else:
        # redirect to login page
        return redirect("/")

# called by "/destroy/<id>" through url(r'^destroy/(?P<id>\d+)$', views.destroy)
def destroy(request, id):
    # if the page is accessed through the dashboard
    if "id" in request.session:
        # delete the user
        x = User.objects.get(id=request.session["id"])
        x.delete()
    # redirect to login page
    return redirect("/")

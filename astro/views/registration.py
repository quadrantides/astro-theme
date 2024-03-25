# coding=utf-8
"""
Created on 2020, May 23th
@author: orion
"""
from django.template import loader
from django.http import HttpResponse

from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate, login

from django.shortcuts import redirect


def logout(request):
    auth_logout(request)
    return redirect("/")


def authentication(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")

    template = loader.get_template('registration/login.html')
    context = dict()
    return HttpResponse(template.render(context, request))

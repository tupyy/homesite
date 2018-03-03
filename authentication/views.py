# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

import json

from django.utils.http import is_safe_url
from django.contrib.auth import authenticate,login,logout

def login_view(request):
    if request.method == 'GET':
        return render(request, 'authentication/login.html',
                      {'login_successful': True,
                       'next': request.GET['next']
                       })

    elif request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            redirect_to = request.POST.get('next')
            url_is_safe = is_safe_url(redirect_to)
            if redirect_to and url_is_safe:
                return HttpResponseRedirect(redirect_to)
            else:
                return redirect("/")
        else:
            return render(request, 'authentication/login.html', {'login_successful': False,
                                                                 'error_message': 'There was a problem with your login'})


def logout_view(request):
    logout(request)
    redirect_to = request.GET.get('next')
    if  redirect_to and is_safe_url(redirect_to):
        return HttpResponseRedirect(redirect_to)
    return redirect('/')
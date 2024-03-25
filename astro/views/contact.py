# coding=utf-8
"""
Created on 2020, May 12th
@author: orion
"""
from django.shortcuts import render


def default_view(request):
    return render(request, 'contact.html')

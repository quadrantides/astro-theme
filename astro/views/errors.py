# coding=utf-8
"""
Created on 2020, May 23th
@author: orion
"""
from django.template import loader
from django.http import HttpResponse


def page_not_found(request, exception=None):
    template = loader.get_template('theme/errors/page_not_found.html')
    context = dict()

    return HttpResponse(template.render(context, request))

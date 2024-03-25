# coding=utf-8
"""
Created on 2020, May 15th
@author: orion
"""
from theme.models import Theme
from theme.forms.celebrities import CelebritiesForm


def get():
    context = dict()
    themes = Theme.objects.all()
    celebrities = []
    for theme in themes:
        celebrity = dict(
            person=theme.get_person(),
            theme_id=theme.id,
        )
        celebrities.append(celebrity)

    context["celebrities"] = celebrities
    context["themes"] = themes
    context['celebrities-form'] = CelebritiesForm()
    return context

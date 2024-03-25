# coding=utf-8
"""
Created on 2020, May 12th
@author: orion
"""
from django.template import loader
from django.http import HttpResponse

from theme.forms.parameters import TropicalForm as TropicalParametersForm
from theme.models import TropicalConfiguration, HousesSystem
from transcend.models.openastro.models import TropicalDefault
from theme.tasks.loading import get_context


def default_view(request):

    template = loader.get_template('index.html')

    if request.method == 'GET':

        configuration = TropicalConfiguration.objects.filter(default=True)[0]
        houses_system = configuration.houses_system

    else:
        id = int(request.POST['houses_system'])
        houses_system = HousesSystem.objects.get(id=id)

    parameters_form = TropicalParametersForm(
        initial=dict(
            houses_system=houses_system,
        ),
    )

    context = {'parameters-form': parameters_form}

    selection = dict(
        tropical=TropicalDefault(houses_system=houses_system.code),
    )

    selection_context = get_context(selection)

    context.update(
        dict(
            graph=selection_context['graphics']['tropical'],
            config=selection_context['graphics']['config'],
        ),
    )

    return HttpResponse(template.render(context, request))

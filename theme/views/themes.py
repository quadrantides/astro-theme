# coding=utf-8
"""
Created on 2020, May 12th
@author: orion
"""
from django.utils.timezone import now

from django.template import loader

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required

from django.template.context_processors import csrf

from theme.models.themes import Theme, Location

from theme.tasks.themes import get_by_keys as get_theme_by_keys
from theme.tasks.locations import get as get_location
from theme.tasks.dates import get_utc_from_timezone, get_utc

from theme.forms.themes import Date as DateForm
from theme.forms.locations import LocationForm
from theme.forms.persons import PersonForm

from transcend.constants import DATE_FORMAT


@login_required(login_url="/accounts/login/")
def save(request):
    context = dict()
    context.update(csrf(request))
    theme = None
    message = ""
    template = loader.get_template('theme/new.html')
    success = False
    if request.method == "POST":
        location_form = LocationForm(request.POST or None)
        person_form = PersonForm(request.POST or None)
        # get utc date
        if "str_date" in request.POST and "str_time" in request.POST:
            utc_date = get_utc_from_timezone(
                request.POST["str_date"],
                request.POST["str_time"],
                request.POST["time_zone"],
            )
        else:
            utc_date = get_utc()

        # if location_form.is_valid() and person_form.is_valid() and date_form.is_valid():
        if location_form.is_valid() and person_form.is_valid():
            person_data = person_form.cleaned_data
            state, theme = get_theme_by_keys(person_data)

            if state.success:

                # calcul du chemin pour la mise à jour de la base de données

                updating_allowed = True

                if theme and request.POST['action'] == 'create':
                    message = "Le thème demandé existe déjà. Veuillez confirmer votre choix de le modifier"
                    updating_allowed = False

                if updating_allowed:

                    data = location_form.cleaned_data
                    state, location = get_location(data)
                    if state.success and not location:
                        location = Location.objects.create(
                            **data,
                        )
                        location.save()

                    data = dict(
                        location=location,
                    )
                    data.update(
                        {"date": utc_date},
                    )
                    theme, created = Theme.objects.update_or_create(
                        **person_data, defaults=data
                    )
                    success = True
                    if theme and request.POST['action'] == 'create':
                        message = "Le thème demandé a été créé"
                    else:
                        message = "Le thème demandé a été modifié"

            else:
                message = "Le thème n'a pas pu être enregistré en raison d'un problème technique"
        else:
            message = "Problème de validation du formulaire : {}".format(
                ", ".join([person_form.errors, date_form.errors, location_form.errors])
            )

        context['person_form'] = person_form
        context['location_form'] = location_form
        # context['date_form'] = date_form
        context['date'] = utc_date.isoformat()
    else:
        context['person_form'] = PersonForm()
        context['location_form'] = LocationForm()
        # context['date_form'] = DateForm()
        context['date'] = now().isoformat()

    if success:
        return HttpResponseRedirect(reverse('theme:theme', args=(theme.id,)))
    else:
        context.update(
            {'success': success, "message": message},
        )
        return HttpResponse(template.render(context, request))


def new(request):
    template = loader.get_template('theme/new.html')
    context = dict()
    context['person_form'] = PersonForm()
    context['location_form'] = LocationForm()
    # context['date_form'] = DateForm()
    context['date'] = now().isoformat()
    context['success'] = True
    return HttpResponse(template.render(context, request))

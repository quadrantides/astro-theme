# coding=utf-8
"""
Created on 2020, May 12th
@author: orion
"""
from datetime import datetime
from django.template import loader
from django.http import HttpResponse
from django.views import generic

from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.timezone import now
from django.utils.timezone import get_current_timezone

from aspects.models import DATE_FORMAT
from theme.tasks.themes import get_by_id as get_theme_by_id

from theme.tasks.celebrities import get as get_celebrities

from theme.forms.parameters import TropicalForm as TropicalParametersForm
from theme.forms.parameters import SiderealForm as SiderealParametersForm
from theme.forms.parameters import AstrologiesParametersForm

from theme.forms.themes import Date as DateForm

from theme.models import Theme, TropicalConfiguration

from theme.tasks.loading import get_context_graphics


class DetailCelebrity(LoginRequiredMixin, generic.DetailView):
    context_object_name = "theme"
    model = Theme
    template_name = 'celebrity/theme.html'
    # transit_start = None
    # transit_end = None
    #
    # def get_object(self, queryset=None):
    #     self.transit_start = self.kwargs.get('start', None)
    #     self.transit_end = self.kwargs.get('end', None)
    #     return queryset.get(slug=self.transit_start)

    def post(self, request, *args, **kwargs):

        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        str_transit_datetime = "{} {}".format(
            request.POST["str_transit_date"],
            request.POST["str_transit_time"]
        )
        # date_form = DateForm(request.POST or None)

        context['transit_date'] = datetime.strptime(str_transit_datetime, DATE_FORMAT)

        if self.request.user.is_authenticated:
            context.update(
                self.get_context_data_for_authenticated_user(context),
            )
        else:
            context.update(
                self.get_context_data_for_anonymous_user(context),
            )

        # context['date_form'] = DateForm()
        date = now()
        context['date'] = date.strftime(DATE_FORMAT)
        date_iso = date.isoformat()
        context['date_iso'] = date_iso

        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):

        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        context['transit_date'] = None

        # context['date_form'] = DateForm()
        date = now()
        context['date'] = date.strftime(DATE_FORMAT)
        transit_date_iso = date.isoformat()
        context['transit_date_iso'] = transit_date_iso
        if self.request.user.is_authenticated:
            context.update(
                self.get_context_data_for_authenticated_user(context),
            )
        else:
            context.update(
                self.get_context_data_for_anonymous_user(context),
            )
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):

        context = super(DetailCelebrity, self).get_context_data(**kwargs)
    #
    #     success = False
    #
    #     # context['transit_date'] = None
    #     #
    #     # if self.request.method == "POST":
    #     #
    #     #     date_form = DateForm(self.request.POST or None)
    #     #
    #     #     if date_form.is_valid():
    #     #
    #     #         date = date_form.cleaned_data
    #     #
    #     #         # is a transit requested ?
    #     #
    #     #         if self.request.path.find('transit') >= 0:
    #     #
    #     #             str_transit_date = self.kwargs.get('transit_date', None)
    #     #
    #     #             if str_transit_date:
    #     #                 try:
    #     #                     context['transit_date'] = datetime.strptime(str_transit_date, DATE_FORMAT)
    #     #
    #     #                 except ValueError:
    #     #                     pass
    #     #
    #     #             else:
    #     #                 context['transit_date'] = datetime.now()
    #     #
    #     # else:
    #     #     context['date_form'] = DateForm()
    #     #     context['date'] = now().strftime(DATE_FORMAT)
    #
    #     # if self.request.user.is_authenticated:
    #     #     context.update(
    #     #         self.get_context_data_for_authenticated_user(context),
    #     #     )
    #     # else:
    #     #     context.update(
    #     #         self.get_context_data_for_anonymous_user(context),
    #     #     )
    #
        return context

    @staticmethod
    def get_context_data_for_anonymous_user(context):

        configuration = TropicalConfiguration.objects.filter(default=True)[0]

        context.update(
            get_context_graphics(context, configuration_tropical=configuration),
        )

        parameters_form = TropicalParametersForm(
            dict(
                houses_system=configuration.houses_system,
            ),
        )

        context['parameters-form'] = parameters_form
        return context

    def get_context_data_for_authenticated_user(self, context):

        profile = self.request.user.profile

        context.update(
            get_context_graphics(
                context,
                configuration_tropical=profile.configuration_tropical,
                configuration_sidereal=profile.configuration_sidereal,
            ),
        )

        active_sidereal_configuration = profile.configuration_sidereal.active if profile.configuration_sidereal else False
        active_tropical_configuration = profile.configuration_tropical.active if profile.configuration_tropical else False

        if active_tropical_configuration and active_sidereal_configuration:
            parameters_form = AstrologiesParametersForm(
                dict(
                    tropical_houses_system=profile.configuration_tropical.houses_system,
                    sidereal_houses_system=profile.configuration_sidereal.houses_system,
                    sidereal_mode=profile.configuration_sidereal.mode,
                ),
            )

        elif active_sidereal_configuration:
            parameters_form = SiderealParametersForm(
                initial=dict(
                    houses_system=profile.configuration_sidereal.houses_system,
                    mode=profile.configuration_sidereal.mode,
                ),
            )

        elif active_tropical_configuration:
            parameters_form = TropicalParametersForm(
                dict(
                    houses_system=profile.configuration_tropical.houses_system,
                ),
            )

        else:
            configuration = TropicalConfiguration.objects.filter(default=True)[0]
            houses_system = configuration.houses_system
            parameters_form = TropicalParametersForm(
                dict(
                    houses_system=houses_system,
                ),
            )
        context['parameters-form'] = parameters_form

        return context


# class CelebrityTransit(generic.DetailView):
#     context_object_name = "theme"
#     model = Theme
#     template_name = 'theme/celebrity.html'
#
#     def get_context_data(self, **kwargs):
#
#         context = super(DetailCelebrity, self).get_context_data(**kwargs)
#
#         if self.request.user.is_authenticated:
#             context.update(
#                 self.get_context_data_for_authenticated_user(context['theme']),
#             )
#         else:
#             context.update(
#                 self.get_context_data_for_anonymous_user(context['theme']),
#             )
#
#         return context
#
#     @staticmethod
#     def get_context_data_for_anonymous_user(theme):
#
#         configuration = TropicalConfiguration.objects.filter(default=True)[0]
#
#         context = get_context_graphics(theme, configuration_tropical=configuration)
#
#         parameters_form = TropicalParametersForm(
#             dict(
#                 houses_system=configuration.houses_system,
#             ),
#         )
#
#         context['parameters-form'] = parameters_form
#         return context
#
#     def get_context_data_for_authenticated_user(self, theme):
#
#         profile = self.request.user.profile
#
#         context = get_context_graphics(
#             theme,
#             configuration_tropical=profile.configuration_tropical,
#             configuration_sidereal=profile.configuration_sidereal,
#         )
#
#         active_sidereal_configuration = profile.configuration_sidereal.active if profile.configuration_sidereal else False
#         active_tropical_configuration = profile.configuration_tropical.active if profile.configuration_tropical else False
#
#         if active_tropical_configuration and active_sidereal_configuration:
#             parameters_form = AstrologiesParametersForm(
#                 dict(
#                     tropical_houses_system=profile.configuration_tropical.houses_system,
#                     sidereal_houses_system=profile.configuration_sidereal.houses_system,
#                     sidereal_mode=profile.configuration_sidereal.mode,
#                 ),
#             )
#
#         elif active_sidereal_configuration:
#             parameters_form = SiderealParametersForm(
#                 initial=dict(
#                     houses_system=profile.configuration_sidereal.houses_system,
#                     mode=profile.configuration_sidereal.mode,
#                 ),
#             )
#
#         elif active_tropical_configuration:
#             parameters_form = TropicalParametersForm(
#                 dict(
#                     houses_system=profile.configuration_tropical.houses_system,
#                 ),
#             )
#
#         else:
#             configuration = TropicalConfiguration.objects.filter(default=True)[0]
#             houses_system = configuration.houses_system
#             parameters_form = TropicalParametersForm(
#                 dict(
#                     houses_system=houses_system,
#                 ),
#             )
#         context['parameters-form'] = parameters_form
#
#         return context


def celebrities(request):

    template = loader.get_template('theme/celebrities.html')
    context = dict()
    context.update(
        get_celebrities(),
    )

    return HttpResponse(template.render(context, request))

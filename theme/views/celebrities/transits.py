# coding=utf-8
"""
Created on 2020, August 28th
@author: orion
"""
import pytz
from datetime import datetime, timezone, timedelta

from django.views import generic
from django.template import loader
from django.http import HttpResponse

from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.timezone import now, get_current_timezone

from aspects.models import DATE_FORMAT

from theme.tasks.celebrities import get as get_celebrities

from theme.forms.parameters import TropicalForm as TropicalParametersForm
from theme.forms.parameters import SiderealForm as SiderealParametersForm
from theme.forms.parameters import AstrologiesParametersForm

from theme.models import Theme, TropicalConfiguration

from theme.tasks.loading import get_context_graphics
from theme.forms.themes import Date as DateForm

tzone = get_current_timezone()


class Detail(LoginRequiredMixin, generic.DetailView):
    context_object_name = "theme"
    model = Theme
    template_name = 'celebrity/transit.html'

    # def post(self, request, *args, **kwargs):
    #     pass

    def get(self, request, *args, **kwargs):

        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        str_date = request.GET["date"] if "date" in request.GET else ""
        str_time = request.GET["time"] if "time" in request.GET else ""
        str_timezone_offset = request.GET["offset"] if "offset" in request.GET else ""
        print(str_timezone_offset)
        str_houses_system = request.GET["houses_system"] if "houses_system" in request.GET else ""

        if str_date and str_time:
            yy = int(str_date[0:4])
            mm = int(str_date[5:7])
            dd = int(str_date[8:10])

            hh = int(str_time[0:2])
            minute = int(str_time[3:5])

            str_transit_date = "{}T{}:00Z".format(
                str_date,
                str_time,
            )
            # transit_date = datetime.strptime(str_transit_date, DATE_FORMAT, tzinfo=tzone)
            local_transit_date = \
                datetime(yy, mm, dd, hh, minute, 0, 0, timezone(timedelta(minutes=-int(str_timezone_offset))))
            utc_transit_date = local_transit_date.astimezone(pytz.utc)
            utc_transit_date_iso = utc_transit_date.isoformat()
        else:
            utc_transit_date = now()
            utc_transit_date_iso = utc_transit_date.isoformat()

        context['date_form'] = DateForm()
        context['transit_date'] = utc_transit_date
        context['utc_transit_date_iso'] = utc_transit_date_iso
        # context['date'] = transit_date.strftime(DATE_FORMAT)

        if self.request.user.is_authenticated:
            context.update(
                self.get_context_data_for_authenticated_user(context),
            )
        else:
            context.update(
                self.get_context_data_for_anonymous_user(context),
            )
        return self.render_to_response(context)

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


def celebrities(request):

    template = loader.get_template('theme/transit/celebrities.html')
    context = dict()
    context.update(
        get_celebrities(),
    )

    return HttpResponse(template.render(context, request))

from django.db import models
from django.utils.translation import ugettext as _

from astro.utils import Timestamp

DATE_FORMAT = "%Y-%m-%d %H:%M"
URL_DATE_FORMAT = "%Y-%m-%dT%H:%M"
UI_DATE_FORMAT = "%d %B %Y"
UI_MONTH_DAY_DATE_FORMAT = "%b-%d"

INTERNAL_CONJUNCTION_TYPES = [_("inferior"), _("superior")]


def validate_angle(value):
    res = 360 + value if value < 0 else value
    return res


def get_cycle_name(planet1, planet2):
    return "{}_{}".format(
        planet1,
        planet2,
    )


def get_aspect_model(cycle_name):

    if cycle_name == "sun_venus":
        model = SunVenusAspect
    elif cycle_name == "sun_mercury":
        model = SunMercuryAspect
    elif cycle_name == "sun_mars":
        model = SunMarsAspect
    elif cycle_name == "saturn_jupiter":
        model = SaturnJupiterAspect
    else:
        raise Exception(
            _("Aborted requested. ASPECT Table undefined for <{}> cycle").format(
                cycle_name,
            )
        )
    return model


def get_conjunction_model(cycle_name):

    model = None
    if cycle_name == "sun_venus":
        model = SunVenusConjunction
    elif cycle_name == "sun_mercury":
        model = SunMercuryConjunction

    return model


def get_coverage_model(cycle_name):

    if cycle_name == "sun_venus":
        model = SunVenusCoverage
    elif cycle_name == "sun_mercury":
        model = SunMercuryCoverage
    elif cycle_name == "sun_mars":
        model = SunMarsCoverage
    elif cycle_name == "saturn_jupiter":
        model = SaturnJupiterCoverage
    else:
        raise Exception(
            _("Aborted requested. COVERAGE Table undefined for <{}> cycle").format(
                cycle_name,
            )
        )
    return model


class Planet(models.Model):

    name = models.CharField(max_length=30, verbose_name=_("Planet"))

    class Meta:
        app_label = 'aspects'

    def __str__(self):
        planet = "{}".format(
            self.name,
        )
        return planet


class Cycle2(models.Model):

    planet1 = \
        models.ForeignKey(
            Planet,
            blank=True,
            null=True,
            on_delete=models.CASCADE,
            verbose_name=_("planet 1"),
            related_name="+",
        )

    planet2 = \
        models.ForeignKey(
            Planet,
            blank=True,
            null=True,
            on_delete=models.CASCADE,
            verbose_name=_("planet 2"),
            related_name="+",
        )

    is_internal = models.BooleanField(
        verbose_name=_("is an internal cycle ?"),
        default=False,
    )

    class Meta:
        app_label = 'aspects'

    description = models.TextField(blank=True, verbose_name=_("more information"))

    def get_name(self):
        return get_cycle_name(self.planet1.name, self.planet2.name)

    def __str__(self):
        planet1 = "{} : {}".format(
            _("planet 1"),
            self.planet1,
        )
        planet2 = "{} : {}".format(
            _("planet 2"),
            self.planet2,
        )

        content = ", ".join(
            [
                planet1,
                planet2,
            ]
        )
        return content


class Orb(models.Model):

    value = models.FloatField(
        verbose_name="orb",
        default=6.0,
    )

    class Meta:
        app_label = 'aspects'

    def __str__(self):
        return str(self.value)


class AbstractAspect(models.Model):

    start = models.DateTimeField()
    true = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField()

    angle = models.FloatField(
        verbose_name="angle",
        default=0.0,
    )

    orb = \
        models.ForeignKey(
            Orb,
            on_delete=models.CASCADE,
            verbose_name="orb",
        )

    active = models.BooleanField(
        verbose_name=_("is an active record ?"),
        default=False,
    )

    class Meta:
        app_label = 'aspects'
        abstract = True

    def get_ui_dates(self):
        return "{} / {}".format(
            self.start.strftime(UI_DATE_FORMAT),
            self.end.strftime(UI_DATE_FORMAT),
        )

    def get_utc_centered_date_iso(self):
        date = self.start + (self.end - self.start) / 2
        return date.isoformat()

    def get_url_end(self):
        return "{}".format(
            _(self.end.strftime(URL_DATE_FORMAT)),
        )

    def get_start(self):
        return "{}".format(
            _(self.start.strftime(UI_DATE_FORMAT)),
        )

    def get_end(self):
        return self.end

    def get_start_year(self):
        return "{}".format(
            self.start.year,
        )

    def get_end_year(self):
        return "{}".format(
            self.end.year,
        )

    def get_start_month_day(self):
        return "{}".format(
            self.start.strftime(UI_MONTH_DAY_DATE_FORMAT),
        )

    def get_end_month_day(self):
        return "{}".format(
            self.end.strftime(UI_MONTH_DAY_DATE_FORMAT),
        )

    def __str__(self):
        angle = "Angle : {}".format(
            str(self.angle),
        )
        orb = "Orb : {}".format(
            str(self.orb),
        )
        start = "{} : {}".format(
            _("Start"),
            str(self.start) if self.start else "",
        )
        end = "{} : {}".format(
            _("End"),
            str(self.end) if self.end else "",
        )
        true = "{} : {}".format(
            _("Exact"),
            str(self.true) if self.true else _("Date not defined"),
        )

        content = ", ".join(
            [
                angle,
                orb,
                start,
                end,
                true,
            ]
        )
        return content


class Aspect2(Timestamp, AbstractAspect):

    cycle = \
        models.ForeignKey(
            Cycle2,
            on_delete=models.CASCADE,
            verbose_name="cycle",
        )

    class Meta:
        app_label = 'aspects'
        abstract = True

    def __str__(self):

        aspect = AbstractAspect.__str__(self)

        cycle = "Cycle : {}".format(
            str(self.cycle),
        )

        content = ", ".join(
            [
                cycle,
                aspect,
            ]
        )
        return content


class InternalConjunction(models.Model):

    type = models.CharField(max_length=150, verbose_name=_("Type"))

    true = models.BooleanField(
        verbose_name=_("Is exact ?"),
        default=False,
    )

    active = models.BooleanField(
        verbose_name=_("is an active record ?"),
        default=False,
    )

    class Meta:
        app_label = 'aspects'
        abstract = True

    def __str__(self):

        conj_type = "{} : {}".format(
            _("Type"),
            str(self.type),
        )
        conj_true = "{} : {}".format(
            _("Is exact ?"),
            _("Yes") if self.true else _("No"),
        )

        content = ", ".join(
            [
                conj_type,
                conj_true,
             ]
        )

        return content


class Coverage(models.Model):

    cycle = \
        models.ForeignKey(
            Cycle2,
            on_delete=models.CASCADE,
            verbose_name="cycle",
            default="",
        )
    start = models.DateTimeField()
    end = models.DateTimeField()

    orb = \
        models.ForeignKey(
            Orb,
            on_delete=models.CASCADE,
            verbose_name="orb",
            default=6,
        )

    angle = models.FloatField(
        verbose_name="angle",
        default=0.0,
    )

    class Meta:
        app_label = 'aspects'
        abstract = True

    def __str__(self):

        cycle = "Cycle : {}".format(
            str(self.cycle),
        )

        start = "Start : {}".format(
            str(self.start) if self.start else "",
        )
        end = "End : {}".format(
            str(self.end) if self.end else "",
        )

        orb = "Orb : {}".format(
            str(self.orb)
        )
        angle = "Angle : {}".format(
            str(self.angle)
        )
        content = ", ".join(
            [
                cycle,
                angle,
                orb,
                start,
                end,
            ]
        )
        return content


class SunVenusAspect(Aspect2):

    class Meta:
        app_label = 'aspects'
        db_table = "sun_venus_aspects"
        ordering = ['-angle', '-orb']


class SunVenusConjunction(InternalConjunction):

    aspect = \
        models.ForeignKey(
            SunVenusAspect,
            blank=True,
            null=True,
            on_delete=models.CASCADE,
            verbose_name="aspect",
        )

    class Meta:
        app_label = 'aspects'
        db_table = "sun_venus_conjunctions"

    def __str__(self):

        return InternalConjunction.__str__(self)


class SunVenusCoverage(Coverage):

    class Meta:
        app_label = 'aspects'
        db_table = "sun_venus_coverages"


class SunMercuryAspect(Aspect2):

    class Meta:
        app_label = 'aspects'
        db_table = "sun_mercury_aspects"
        ordering = ['-angle', '-orb']


class SunMercuryConjunction(InternalConjunction):

    aspect = \
        models.ForeignKey(
            SunMercuryAspect,
            blank=True,
            null=True,
            on_delete=models.CASCADE,
            verbose_name="aspect",
        )

    class Meta:
        app_label = 'aspects'
        db_table = "sun_mercury_conjunctions"

    def __str__(self):

        return InternalConjunction.__str__(self)


class SunMercuryCoverage(Coverage):

    class Meta:
        app_label = 'aspects'
        db_table = "sun_mercury_coverages"


class SunMarsAspect(Aspect2):

    class Meta:
        app_label = 'aspects'
        db_table = "sun_mars_aspects"
        ordering = ['-angle', '-orb']


class SunMarsCoverage(Coverage):

    class Meta:
        app_label = 'aspects'
        db_table = "sun_mars_coverages"


class SaturnJupiterAspect(Aspect2):

    class Meta:
        app_label = 'aspects'
        db_table = "saturn_jupiter_aspects"
        ordering = ['-angle', '-orb']


class SaturnJupiterCoverage(Coverage):

    class Meta:
        app_label = 'aspects'
        db_table = "saturn_jupiter_coverages"

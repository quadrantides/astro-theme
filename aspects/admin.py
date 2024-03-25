from django.contrib import admin

from .models import Planet
from .models import Cycle2
from .models import Orb

from .models import SunVenusAspect
from .models import SunVenusConjunction
from .models import SunVenusCoverage

from .models import SunMercuryAspect
from .models import SunMercuryConjunction
from .models import SunMercuryCoverage

from .models import SunMarsAspect
from .models import SunMarsCoverage

from .models import SaturnJupiterAspect
from .models import SaturnJupiterCoverage

admin.site.register(Planet)
admin.site.register(Cycle2)
admin.site.register(Orb)

admin.site.register(SunVenusAspect)
admin.site.register(SunVenusConjunction)
admin.site.register(SunVenusCoverage)

admin.site.register(SunMercuryAspect)
admin.site.register(SunMercuryConjunction)
admin.site.register(SunMercuryCoverage)

admin.site.register(SunMarsAspect)
admin.site.register(SunMarsCoverage)

admin.site.register(SaturnJupiterAspect)
admin.site.register(SaturnJupiterCoverage)

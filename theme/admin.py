from django.contrib import admin

from .models import Location
from .models import Theme
from .models import HousesSystem
from .models import SiderealMode
from .models import Profile
from .models import TropicalConfiguration
from .models import SiderealConfiguration
from .models import AstroConfiguration

admin.site.register(Profile)

admin.site.register(Location)
admin.site.register(Theme)

admin.site.register(HousesSystem)
admin.site.register(SiderealMode)

admin.site.register(TropicalConfiguration)
admin.site.register(SiderealConfiguration)
admin.site.register(AstroConfiguration)

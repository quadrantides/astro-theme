"""astro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin

from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.views import PasswordResetView

from django.urls import path, include

from astro.views import errors
from astro.views import contact
from astro.views import index

from astro.views.webservices import geonames
from astro.views.registration import authentication

handler404 = errors.page_not_found

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('authentication/', authentication, name='authentication'),
    path('password_reset', PasswordResetView.as_view(), name='password_reset'),
    path('', index.default_view, name='index'),
    path('contact/', contact.default_view, name='contact'),
    path('geo/service/', geonames.default_view, name='geoname'),
    path('theme/', include('theme.urls')),
    path('aspects/', include('aspects.urls')),
]

# bokeh_base_path = settings.BOKEH_BASE_PATH
#
# bokeh_apps = [
#     document("aspects/activation", views.activation_view),
# ]
#
#
# urlpatterns += static_extensions()
# urlpatterns += staticfiles_urlpatterns()

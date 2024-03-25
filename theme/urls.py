from django.urls import path

from theme.views.celebrities import themes as celebrities_themes
from theme.views.celebrities import transits as celebrities_transits
from .views import themes
from .views.reports import generate_pdf

app_name = 'theme'


urlpatterns = [

    path('', celebrities_themes.celebrities, name='celebrities'),

    path('<int:pk>/', celebrities_themes.DetailCelebrity.as_view(), name='theme'),

    path('new/', themes.new, name='new'),
    path('save/', themes.save, name='save'),
    # path('transit/', celebrities.DetailCelebrity.as_view(), name='transit'),
    path('<int:theme_id>/report/', generate_pdf, name='generate_pdf'),

    path('transit/', celebrities_transits.celebrities, name='transit_celebrities'),
    path(
        'transit/<int:pk>/',
        celebrities_transits.Detail.as_view(),
        name='transit',
    ),
    path(
        'transit/',
        celebrities_transits.Detail.as_view(),
        name='celebrity_transit',
    ),
]

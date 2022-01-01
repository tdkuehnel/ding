from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'benutzer'

urlpatterns = [
    path('anmeldung/',                                        views.DingLoginView.as_view(),             name='anmeldung'),
    path('abmeldung/',                                        views.DingLogoutView.as_view(),            name='abmeldung'),
]

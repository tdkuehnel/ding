from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core import mail
from django.test import TestCase
from django_webtest import WebTest
from django.urls import reverse

from .models import Benutzer

from .testhilfen import create_benutzer

import datetime

# Create your tests here.

class BenutzerFunctionalTest(TestCase):

    def disabled_test_passwort_reset(self):
        """ Test Passwort reset Funktionalität"""
        benutzer = create_benutzer('name123', 'kennwort')
        credentials = {'username': 'name123', 'password': 'falscheskennwort' }
        response = self.client.post('/anmeldung/', credentials, follow=True)
        self.assertFalse(response.context['user'].is_authenticated)


    def test_benutzer(self):
        """ Test von Benutzer"""
        benutzer = create_benutzer('name123', 'kennwort')
        self.assertIsNotNone(benutzer)

        credentials = {'username': 'name123', 'password': 'kennwort' }

        response = self.client.post('/anmeldung/', credentials, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)

        response = self.client.get('/abmeldung/', follow=True)
        self.assertFalse(response.context['user'].is_authenticated)

        credentials = {'username': 'name123', 'password': 'kennwort' }
        response = self.client.post('/anmeldung/', credentials, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)
        #pretty(response.content)

    def test_profil(self):
        # Zwei Benutzer erzeugen
        benutzer = create_benutzer('name123', 'kennwort')
        benutzer2 = create_benutzer('name234', 'andereskennwort')
        self.assertIsNotNone(benutzer)
        self.assertIsNotNone(benutzer2)

        # Zugriff auf Profilseite darf nicht möglich sein ohne Anmeldung
        #response = self.client.get('/benutzer/profil/'+str(benutzer.id)+'/', follow=True)
        #self.assertIn(b'404', response.content)

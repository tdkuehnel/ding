#!/usr/bin/env python
import os
import sys

# Django initialization
import django
from django.conf import settings
#import ding.settings as app_settings

sys.path.append(
    os.path.join(os.path.dirname(__file__), 'ding')
)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ding.settings")

from django.conf import settings
django.setup()

# wxPtyhon main module
import Main
Main.main()

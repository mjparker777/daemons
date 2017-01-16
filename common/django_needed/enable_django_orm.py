"""
    NOTE: Only import this from code that is not part of the Django server.
    This will setup Django ORM, templates, etc so they can be used from outside of the server.
"""
import os
import sys

import django

from common import constants

sys.path.append(os.path.abspath(constants.PYTHON_PROJECT_PATH))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_project.settings")
django.setup()

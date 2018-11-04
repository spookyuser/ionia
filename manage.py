#!/usr/bin/env python

"""Slightly different manage.py

Modified to suit django-configurations:
https://django-configurations.readthedocs.io/en/stable/#quickstart
"""

import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ionia.settings")
    os.environ.setdefault("DJANGO_CONFIGURATION", "Dev")

    from configurations.management import execute_from_command_line

    execute_from_command_line(sys.argv)

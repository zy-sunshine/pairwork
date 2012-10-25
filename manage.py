#!/usr/bin/env python
import os
import sys
ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(ROOT_PATH, 'pairwork', 'apps'))
if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pairwork.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

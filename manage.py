#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

projName = 'stylesense_proj'
root_path = os.path.abspath(os.path.join(os.path.realpath(__file__), '..', '..'))
sys.path.insert(0, os.path.abspath(os.path.join(root_path, projName)))
sys.path.insert(0, os.path.abspath(os.path.join(root_path, projName, projName)))
sys.path.insert(0, os.path.abspath(os.path.join(root_path, projName, projName, 'apps')))


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stylesense_proj.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

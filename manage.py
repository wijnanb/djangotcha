#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    try:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangotcha.settings")

        from django.core.management import execute_from_command_line
        execute_from_command_line(sys.argv)
    except:
        import traceback
        print traceback.format_exc()

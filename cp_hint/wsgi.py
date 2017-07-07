"""
WSGI config for cp_hint project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
import time
import trackback
import signal
import sys
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cp_hint.settings")

try:
    application = get_wsgi_application()
except:
    print ('handing WSGI exception')

    if 'mod_wsgi' in sys.modules:
        trackback.print_exc()
        os.kill(os.getpid(), signal.SIGINT)
        time.sleep(2.5)

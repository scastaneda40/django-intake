import os
import logging
from django.core.wsgi import get_wsgi_application

logger = logging.getLogger('wsgi')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

logger.debug("Starting WSGI application...")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'counseling_app.settings')

application = get_wsgi_application()

logger.debug("WSGI application loaded successfully.")

import os
import sys
from django.core.wsgi import get_wsgi_application

sys.path.append('/home/heinz/pyprojects')
sys.path.append('/home/heinz/pyprojects/heinz_signup')
sys.path.append('/home/heinz/pyprojects/heinz_signup/heinz_signup')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'heinz_signup.settings')

application = get_wsgi_application()

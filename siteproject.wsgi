import os
import sys
import site

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('~/.virtualenvs/webapps/local/lib/python2.7/site-packages')

# Add the app's directory to the PYTHONPATH

# first append the project folder path
sys.path.append('/var/www/siteproject')

# second append the location of the app settings.py file note the case sensitive path. 
sys.path.append('/var/www/siteproject/siteproject')

# Note that siteproject.settings corresponds with the folder name of the settings.py file. 
os.environ['DJANGO_SETTINGS_MODULE'] = 'siteproject.settings'

# Activate your virtual env
activate_env=os.path.expanduser("/home/danny/.virtualenvs/webapps/bin/activate_this.py")
execfile(activate_env, dict(__file__=activate_env))

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

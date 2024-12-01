import sys
import os
import django

sys.path.append('/home/user12/Project/work/accountantmatchmaking_project')

os.environ['DJANGO_SETTINGS_MODULE'] = 'accountantmatchmaking_project.settings'
django.setup()
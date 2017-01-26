## This file will delete the data in the database and recreate the database without any data 
## To insert more data run the initialize.py file

#!/usr/bin/env python3

from django.core import management
from django.db import connection
from datetime import datetime
import os, os.path, sys


# ensure the user really wants to do this
areyousure = input('''
  You are about to drop and recreate the entire database.
  All data are about to be deleted.  Use of this script
  may cause itching, vertigo, dizziness, tingling in
  extremities, loss of balance or coordination, slurred
  speech, temporary zoobie syndrome, longer lines at the
  testing center, changed passwords in Learning Suite, or
  uncertainty about whether to call your professor
  'Brother' or 'Doctor'.

  Please type 'yes' to confirm the data destruction: ''')
if areyousure.lower() != 'yes':
    print()
    print('  Wise choice.')
    sys.exit(1)

# initialize the django environment
os.environ['DJANGO_SETTINGS_MODULE'] = 'fomo.settings'
import django
django.setup()


# drop and recreate the database tables
print()
print('Living on the edge!  Dropping the current database tables.')
with connection.cursor() as cursor:
    cursor.execute("DROP SCHEMA public CASCADE")
    cursor.execute("CREATE SCHEMA public")
    cursor.execute("GRANT ALL ON SCHEMA public TO postgres")
    cursor.execute("GRANT ALL ON SCHEMA public TO public")

# make the migrations and migrate
management.call_command('makemigrations')
management.call_command('migrate')




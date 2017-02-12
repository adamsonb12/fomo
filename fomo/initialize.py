import os
# initialize the django environment
os.environ['DJANGO_SETTINGS_MODULE'] = 'fomo.settings'
import django
django.setup()

# for our project
from django.contrib.auth.models import Permission, Group
from datetime import datetime
from decimal import Decimal

from account import models as amod #account models
from catalog import models as cmod #catalog models

# Create some default permissions

# Create our Groups

g1 = Group()
g1.name = 'Salespeople'
g1.save()
g1.permissions.add(Permission.objects.get(codename='add_fomouser'))
g1.permissions.add(Permission.objects.get(codename='change_fomouser'))
g1.permissions.add(Permission.objects.get(codename='delete_fomouser'))

# Create 4 users below with variables // Only run if the database has been cleared or the following users have been commented out

user1 = amod.FomoUser()

user1.set_password = "password"
user1.username = "user1"
user1.first_name = "Cassie"
user1.last_name = "Adamson"
user1.email = "user1@byu.edu"
user1.birth_date = datetime(1996,2,2)
user1.gender = "female"
user1.is_staff = True
user1.is_superuser = True
user1.save()

user2 = amod.FomoUser()

user2.set_password = "password"
user2.username = "user2"
user2.first_name = "Brooke"
user2.last_name = "Harrison"
user2.email = "user2@byu.edu"
user2.birth_date = datetime(1994,6,17)
user2.gender = "other"
user2.save()

user3 = amod.FomoUser()

user3.set_password = "password"
user3.username = "user3"
user3.first_name = "Brett"
user3.last_name = "Adamson"
user3.email = "user3@byu.edu"
user3.birth_date = datetime(1993,5,11)
user3.gender = "male"
user3.save()

user4 = amod.FomoUser()

user4.set_password = "password"
user4.username = "user4"
user4.first_name = "Trently"
user4.last_name = "Harrison"
user4.email = "user4@byu.edu"
user4.birth_date = datetime(1992,8,14)
user4.gender = "female"
user4.save()

p = Permission.objects.get(codename='add_fomouser')
user1.user_permissions.add(p) # gives user1 the permission to add users

# ## prints all the users' genders with the gender 'Other'
# users = FomoUser.objects.filter(gender='other')
# for u in users:
# 	print(u.first_name)

# ## gets a user witht the username "user3" and prints it
# u1 = FomoUser.objects.get(username='user3')
# print('My name is ' + u1.first_name + ' ' + u1.last_name + ' and my password is ' + u1.password)

# ## prints all users who have "M" as their gender
# users = FomoUser.objects.filter(gender='male')
# for u in users:
# 	print(u.username)

# ## prints all the users who do not have the username "user4"
# users = FomoUser.objects.exclude(username='user4')
# for u in users:
# 	print(u.last_name)

# Cerate a category
cat1 = cmod.Category()
cat1.codename = 'kids'
cat1.name = 'Kids Toy Products'
cat1.save()

# Create a Bulk Product
p1 = cmod.BulkProduct()
p1.name = 'Kazoo'
p1.category = cat1
p1.price = Decimal('9.50')
p1.quantity = 20
p1.reorder_trigger = 5
p1.reorder_quantity = 30
p1.save()





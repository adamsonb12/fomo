import os
from datetime import datetime
# initialize the django environment
os.environ['DJANGO_SETTINGS_MODULE'] = 'fomo.settings'
import django
django.setup()
from account.models import FomoUser #account models

# Create 4 users below with variables // Only run if the database has been cleared or the following users have been commented out

user1 = FomoUser()

user1.set_password = "password"
user1.username = "user1"
user1.first_name = "Cassie"
user1.last_name = "Adamson"
user1.email = "user1@byu.edu"
user1.birth_date = datetime(1996,2,2)
user1.gender = "female"
user1.save()

user2 = FomoUser()

user2.set_password = "password"
user2.username = "user2"
user2.first_name = "Brooke"
user2.last_name = "Harrison"
user2.email = "user2@byu.edu"
user2.birth_date = datetime(1994,6,17)
user2.gender = "other"
user2.save()

user3 = FomoUser()

user3.set_password = "password"
user3.username = "user3"
user3.first_name = "Brett"
user3.last_name = "Adamson"
user3.email = "user3@byu.edu"
user3.birth_date = datetime(1993,5,11)
user3.gender = "male"
user3.save()

user4 = FomoUser()

user4.set_password = "password"
user4.username = "user4"
user4.first_name = "Trently"
user4.last_name = "Harrison"
user4.email = "user4@byu.edu"
user4.birth_date = datetime(1992,8,14)
user4.gender = "female"
user4.save()

## prints all the users' genders with the gender 'Other'
users = FomoUser.objects.filter(gender='other')
for u in users:
	print(u.first_name)

## gets a user witht the username "user3" and prints it
u1 = FomoUser.objects.get(username='user3')
print('My name is ' + u1.first_name + ' ' + u1.last_name + ' and my password is ' + u1.password)

## prints all users who have "M" as their gender
users = FomoUser.objects.filter(gender='male')
for u in users:
	print(u.username)

## prints all the users who do not have the username "user4"
users = FomoUser.objects.exclude(username='user4')
for u in users:
	print(u.last_name)













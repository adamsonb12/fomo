import os
from datetime import datetime
# initialize the django environment
os.environ['DJANGO_SETTINGS_MODULE'] = 'fomo.settings'
import django
django.setup()
from account.models import FomoUser #account models

# Create 4 users below with variables

# user1 = FomoUser()

# user1.password = "password"
# user1.username = "user1"
# user1.first_name = "user"
# user1.last_name = "1"
# user1.email = "user1@byu.edu"
# user1.birth_date = datetime(1996,2,2)
# user1.gender = "M"
# user1.save()

# user2 = FomoUser()

# user2.password = "password"
# user2.username = "user2"
# user2.first_name = "user"
# user2.last_name = "2"
# user2.email = "user2@byu.edu"
# user2.birth_date = datetime(1994,6,17)
# user2.gender = "F"
# user2.save()

# user3 = FomoUser()

# user3.password = "password"
# user3.username = "user3"
# user3.first_name = "user"
# user3.last_name = "3"
# user3.email = "user3@byu.edu"
# user3.birth_date = datetime(1993,5,11)
# user3.gender = "M"
# user3.save()

# user4 = FomoUser()

# user4.password = "password"
# user4.username = "user4"
# user4.first_name = "user"
# user4.last_name = "4"
# user4.email = "user4@byu.edu"
# user4.birth_date = datetime(1992,8,14)
# user4.gender = "F"
# user4.save()

## prints all the users' genders with the gender 'Unknown'
# users = FomoUser.objects.filter(gender='unknown')
# for u in users:
# 	print(u.gender)

## gets a user witht the username "user3" and prints it
# u1 = FomoUser.objects.get(username='user3')
# print('My name is ' + u1.first_name + ' ' + u1.last_name + ' and my password is ' + u1.password)

## prints all users who have "M" as their gender
# users = FomoUser.objects.filter(gender='M')
# for u in users:
# 	print(u.username)

## prints all the users who do not have the username "user4"
# users = FomoUser.objects.exclude(username='user4')
# for u in users:
# 	print(u.last_name)













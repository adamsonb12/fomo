import os
# initialize the django environment
os.environ['DJANGO_SETTINGS_MODULE'] = 'fomo.settings'
import django
django.setup()

# for our project
from django.contrib.auth.models import Permission, Group
from datetime import datetime
from decimal import Decimal
import json as json

from account import models as amod #account models
from catalog import models as cmod #catalog models

# Create some default permissions

# Create our Groups

g1 = Group()
g1.name = 'Customer'
g1.save()
g1.permissions.add(Permission.objects.get(codename='add_fomouser'))
g1.permissions.add(Permission.objects.get(codename='change_fomouser'))

g2 = Group()
g2.name = 'Employee'
g2.save()
g2.permissions.add(Permission.objects.get(codename='add_fomouser'))
g2.permissions.add(Permission.objects.get(codename='change_fomouser'))
g2.permissions.add(Permission.objects.get(codename='change_bulkproduct'))

g3 = Group()
g3.name = 'Manager'
g3.save()
g3.permissions.add(Permission.objects.get(codename='add_fomouser'))
g3.permissions.add(Permission.objects.get(codename='change_fomouser'))
g3.permissions.add(Permission.objects.get(codename='delete_fomouser'))
g3.permissions.add(Permission.objects.get(codename='add_uniqueproduct'))
g3.permissions.add(Permission.objects.get(codename='change_uniqueproduct'))
g3.permissions.add(Permission.objects.get(codename='delete_uniqueproduct'))
g3.permissions.add(Permission.objects.get(codename='add_bulkproduct'))
g3.permissions.add(Permission.objects.get(codename='delete_bulkproduct'))
g3.permissions.add(Permission.objects.get(codename='change_bulkproduct'))
g3.permissions.add(Permission.objects.get(codename='add_rentalproduct'))
g3.permissions.add(Permission.objects.get(codename='change_rentalproduct'))
g3.permissions.add(Permission.objects.get(codename='delete_rentalproduct'))

# Create 4 users below with variables // Only run if the database has been cleared or the following users have been commented out

user1 = amod.FomoUser()

user1.set_password("password")
user1.username = "user1"
user1.first_name = "Cassie"
user1.last_name = "Adamson"
user1.email = "user1@byu.edu"
user1.birth_date = datetime(1996,2,2)
user1.gender = "female"
user1.is_staff = True
user1.is_superuser = True
user1.save()

user1.groups.add(g3)

user2 = amod.FomoUser()

user2.set_password("password")
user2.username = "user2"
user2.first_name = "Brooke"
user2.last_name = "Harrison"
user2.email = "user2@byu.edu"
user2.birth_date = datetime(1994,6,17)
user2.gender = "other"
user2.save()

user2.groups.add(g2)

user3 = amod.FomoUser()

user3.set_password("password")
user3.username = "user3"
user3.first_name = "Brett"
user3.last_name = "Adamson"
user3.email = "user3@byu.edu"
user3.birth_date = datetime(1993,5,11)
user3.gender = "male"
user3.save()

user3.groups.add(g3)

user4 = amod.FomoUser()

user4.set_password("password")
user4.username = "user4"
user4.first_name = "Trently"
user4.last_name = "Harrison"
user4.email = "user4@byu.edu"
user4.birth_date = datetime(1992,8,14)
user4.gender = "female"
user4.save()

user4.groups.add(g1)

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

# Create a category
cat1 = cmod.Category()
cat1.codename = 'br'
cat1.name = 'Brass'
cat1.save()

# Create a category
cat2 = cmod.Category()
cat2.codename = 'wd'
cat2.name = 'Wood Winds'
cat2.save()

# Create a category
cat3 = cmod.Category()
cat3.codename = 'pc'
cat3.name = 'Percussion'
cat3.save()

# Create a category
cat4 = cmod.Category()
cat4.codename = 'ac'
cat4.name = 'Accessories'
cat4.save()

# Create a category
cat5 = cmod.Category()
cat5.codename = 'st'
cat5.name = 'Strings'
cat5.save()

# products = cmod.Product.objects.all()

# Create a Unique Product
p1 = cmod.UniqueProduct()
p1.product = p1
p1.serial_number = '1234asdf'
p1.name = 'Violin'
p1.category = cat5
p1.price = Decimal('250.99')
dList = ['Violin hand made in 1456', 'Played be Bach and Beethoved', 'Korys favorite instrument']
p1.descriptionList = json.dumps(dList)
iList = ['/static/homepage/media/img/violin.jpg', '/static/homepage/media/img/violin2.png', '/static/homepage/media/img/violin3.jpg', '/static/homepage/media/img/thumbnail_violin.jpg']
p1.imgList = json.dumps(iList)
p1.save()

# Create a Unique Product
p2 = cmod.UniqueProduct()
p2.product = p2
p2.serial_number = '3456asdf'
p2.name = 'Clarinet'
p2.category = cat2
p2.price = Decimal('199.99')
dList = ['Clarinet from Mordor', 'Played by Sauron and his minions', 'Alexs favorite instrument']
p2.descriptionList = json.dumps(dList)
iList = ['/static/homepage/media/img/clar1.jpg', '/static/homepage/media/img/clar2.jpg']
p2.imgList = json.dumps(iList)
p2.save()

# Create a Unique Product
p3 = cmod.UniqueProduct()
p3.product = p3
p3.serial_number = '2345asdf'
p3.name = 'Trumpet'
p3.category = cat1
p3.price = Decimal('250.99')
dList = ['Trumpet forged in the fires of Mount Doom', 'Isuldurs Bane', 'The instrument to rule them all', 'It is shiny']
p3.descriptionList = json.dumps(dList)
iList = ['/static/homepage/media/img/trump1.jpg', '/static/homepage/media/img/trump2.jpg', '/static/homepage/media/img/trump3.png', '/static/homepage/media/img/trump4.png']
p3.imgList = json.dumps(iList)
p3.save()

# Create a Bulk Product
p4 = cmod.BulkProduct()
p4.name = 'Sheet Music 1'
p4.category = cat4
p4.price = Decimal('9.50')
p4.quantity = 20
p4.reorder_trigger = 5
p4.reorder_quantity = 30
dList = ['Holy sheet music', 'From Beethoven to T-swizzle']
p4.descriptionList = json.dumps(dList)
iList = ['/static/homepage/media/img/sh1.jpg', '/static/homepage/media/img/sh2.jpg', '/static/homepage/media/img/sh3.png']
p4.imgList = json.dumps(iList)
p4.save()

# Create a Bulk Product
p5 = cmod.BulkProduct()
p5.name = 'Spare Part 1'
p5.category = cat4
p5.price = Decimal('12.50')
p5.quantity = 12
p5.reorder_trigger = 2
p5.reorder_quantity = 10
dList = ['Spare part for anything', 'Seriously, anything, examples below', 'Spare part for Car', 'Spare part for your instruemt', 'spare part for your body']
p5.descriptionList = json.dumps(dList)
iList = ['/static/homepage/media/img/sp1.jpg', '/static/homepage/media/img/sp2.jpg']
p5.imgList = json.dumps(iList)
p5.save()

# Create a Bulk Product
p6 = cmod.BulkProduct()
p6.name = 'Drum Sticks'
p6.category = cat3
p6.price = Decimal('5.50')
p6.quantity = 30
p6.reorder_trigger = 10
p6.reorder_quantity = 30
dList = ['Best dang drumsticks on this earth', 'Never touched by Obama', 'Very conservative, unlike most drumsticks']
p6.descriptionList = json.dumps(dList)
iList = ['/static/homepage/media/img/drum1.png', '/static/homepage/media/img/drum3.jpg']
p6.imgList = json.dumps(iList)
p6.save()

# Create a Rental Product
p7 = cmod.RentalProduct()
p7.product = p7
p7.serial_number = '1357asdf'
p7.name = 'Trumpet'
p7.category = cat1
p7.price = Decimal('12.99')
dList = ['Rent this Brass', 'My Brass is better than your rental brass', 'Trump Trumps the Trumpet']
p7.descriptionList = json.dumps(dList)
iList = ['/static/homepage/media/img/trump1.jpg', '/static/homepage/media/img/trump2.jpg', '/static/homepage/media/img/trump3.png', '/static/homepage/media/img/trump4.png']
p7.imgList = json.dumps(iList)
p7.save()

# Create a Rental Product
p8 = cmod.RentalProduct()
p8.product = p8
p8.serial_number = '2468asdf'
p8.name = 'Tuba'
p8.category = cat1
p8.price = Decimal('16.99')
dList = ['The Tuba from Tattoine', 'Help me Tuba, youre my only hope', 'Han Solos favorite instrument', 'Spoiler, he died']
p8.descriptionList = json.dumps(dList)
iList = ['/static/homepage/media/img/tuba1.jpg', '/static/homepage/media/img/tuba2.jpg', '/static/homepage/media/img/tuba3.jpg']
p8.imgList = json.dumps(iList)
p8.save()

# Create a Rental Product
p9 = cmod.RentalProduct()
p9.product = p9
p9.serial_number = '9876asdf'
p9.name = 'Trombone'
p9.category = cat1
p9.price = Decimal('11.99')
dList = ['Brass Trombone', 'Made in the Mustafar System', 'Darth Vaders least favorite instrument']
p9.descriptionList = json.dumps(dList)
iList = ['/static/homepage/media/img/trom1.jpg', '/static/homepage/media/img/trom2.jpg']
p9.imgList = json.dumps(iList)
p9.save()


# for p in Permission.objects.all():
# 	print(p)





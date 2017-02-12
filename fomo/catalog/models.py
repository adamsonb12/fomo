from django.db import models
from polymorphic.models import PolymorphicModel

# Create your models here.

# 3 Inerhitance Types

# 1. Class Inheritance (4 tables)
# 	Can create a Product
# 	Splits the data across two tables
# 	Primary keys are equal, also serve as foreign keys
#	1a. Polymorphic Inheritance (4 tables)

# 2. Abstract Inheritance (3 tables)
# 	Cannot create a Product
# 	Each subtable has all fields
# 	Product (doesnt exist)
# 	UP all fields
# 	BP all fields (some duplications of UP)
# 	RP all fields (some duplications of UP)
# 	Primary keys are just primary keys because 1 table

# 3. Composition (4 tables)
# 	The noraml relationship way - 0 - 1
# 	Primary keys from product table is foreign key in subtable
# 	Primary key in product is not the same as primary key in subtable
# 	Two pbjects in memory to represent a real world thing

## By Monday -> Make all these work and add a few of each inthe intialize.py file
# Color tool -> Webaim


class Category(models.Model):
	# id
	codename = models.TextField(blank=True, null=True)
	name = models.TextField(blank=True, null=True)


class Product(PolymorphicModel):
	# id
	name = models.TextField(blank=True, null=True)
	category = models.ForeignKey('Category')
	price = models.DecimalField(max_digits=8, decimal_places=2)
	create_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(auto_now=True)
	class Meta:
		abstract = True;


class BulkProduct(Product):
	# id
	# name
	# category
	# price
	quantity = models.IntegerField()
	reorder_trigger = models.IntegerField()
	reorder_quantity = models.IntegerField()


class UniqueProduct(Product):
	# id
	# name
	# category
	# price
	serial_number = models.TextField()


class RentalProduct(Product):
	# id
	# name
	# category
	# price
	serial_number = models.TextField()

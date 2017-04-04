from django.db import models
from polymorphic.models import PolymorphicModel
from account import models as amod
from django.http import HttpResponse, HttpResponseRedirect

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
	codename = models.TextField(blank=True, null=True, unique=True)
	name = models.TextField(blank=True, null=True)

	def __str__(self):
		return self.codename + ': ' + self.name


class Product(PolymorphicModel):
	# id
	name = models.TextField(blank=True, null=True)
	category = models.ForeignKey('Category')
	price = models.DecimalField(max_digits=8, decimal_places=2)
	create_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(auto_now=True)
	imgList = models.TextField(null=True) # JSON-serialized (text) version of your list
	descriptionList = models.TextField(null=True) # JSON-serialized (text) version of your list



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
	sold = models.BooleanField(default=False)
	available = models.BooleanField(default=True)


class RentalProduct(Product):
	# id
	# name
	# category
	# price
	serial_number = models.TextField()
	sold = models.BooleanField(default=False)
	available = models.BooleanField(default=True)

# More models connected to the User

class ProductHistory(models.Model):
	user = models.ForeignKey('account.FomoUser', on_delete=models.CASCADE ,related_name="user")
	product = models.ForeignKey('catalog.Product')
	view_date = models.DateTimeField(auto_now_add=True)

	# def getLastFive(user):

		# Convienence Methods
		
		# Logic here to get and return the last 5 viewed products


class ShoppingCart(models.Model):
	user = models.ForeignKey('account.FomoUser', on_delete=models.CASCADE, related_name="cart")
	product = models.ForeignKey('catalog.Product', null=True)
	quantity = models.IntegerField(default=1)
	date_added = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(auto_now=True)

	# Convienence Methods

	# add item to cart
	def addItem(uid, pid, quantity):
		try:
			user = amod.objects.get(id=uid)
			product = Product.objects.get(id=pid)
		except:
			return HttpResponseRedirect('/catalog/index/')	
		self.user = user

		# check product availability 
		if hasattr(product, 'quantity'):
			if product.quantity < quantity:
				return False
			self.product = product
			self.product.quantity = quantity
			product.quantity -= quantity
			product.save()
		if hasattr(product, 'available'):
			self.product = product
			product.available = False
			product.save()
		

	# remove item from cart
	# clear cart
	# Retrieve Items
	# Calculate Tax
	# Calculate Subtotal
	# Number of items in cart

class Sale(models.Model):
	user = models.ForeignKey('account.FomoUser', related_name="sales")
	sale_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(auto_now=True)
	sale_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
	total_tax = models.DecimalField(max_digits=8, decimal_places=2, default=0)

	# Convienence Methods

	# # Create a record_sale() method in your models.py file.  
	# This method should 1) create a Sale object, 2) 
	# create one or more SaleItem objects for the purchases, 
	# 4) create a 
	# Payment object, 5) update BulkProduct quantities and IndividualProduct availability.

	@staticmethod
	def record_sale(user, cart_items_list, address, city, state, zipcode, stripe_charge_token):

		# call stripe API, pass the token, and see if it returns true or false stripeResponse = 

		# this if statement would check to see if the token is valid at stripe
		if stripeResponse:
			# If the stripe API returns true
			sale = Sale()
			sale.user = user

			try:

				for item in cart_items_list:
					sale_item = SaleItem()
					sale_item.sale = sale
					sale_item.product = item.product
					sale_item.quantity = item.quantity
					sale_item.sale_price = item.product.sale_price
					#call convienence method to get tax amountsale_item.tax_amount = 
					sale_item.discount = item.discount
					sale_item.save()
					sale.sale_price = sale.sale_price + sale_item.sale_price
					sale.total_tax = sale.total_tax + sale_item.tax_amount
					if hasattr(item.product, 'quantity'):
						item.product.quantity -= item.quantity
					if hasattr(item.product, 'sold'):
						item.product.sold = True

					item.product.save()

				sale.save()

				payment = Payment()
				payment.sale = sale
				payment.total_paid = sale.price
				payment.save()

				shipping = amod.ShippingAddress()
				shipping.shipping_address = address
				shipping.shipping_city = city
				shipping.shipping_state = state
				shipping.shipping_zipcode = zipcode

				shipping.save()

				return True

			except BaseException:
				return False

		# Returns false if stripe returned false
		return False


	# Convienence Methods

class SaleItem(models.Model):
	sale = models.ForeignKey('Sale', on_delete=models.CASCADE, related_name='sale')
	product = models.ForeignKey('Product', related_name='saleitems', null=True)
	quantity = models.IntegerField(default=1)
	sale_price = models.DecimalField(max_digits=8, decimal_places=2)
	discount = models.DecimalField(max_digits=8, decimal_places=2, null=True)
	tax = models.DecimalField(max_digits=8, decimal_places=2, default=7.25)
	tax_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)

	# Convienence Methods

	# Calc Price

class Payment(models.Model):
	sale = models.ForeignKey('Sale', on_delete=models.CASCADE, related_name='payments')
	total_paid = models.DecimalField(max_digits=8, decimal_places=2)
	payment_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(auto_now=True)

	# Convienence Methods














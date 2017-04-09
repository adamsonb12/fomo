from django.db import models
from polymorphic.models import PolymorphicModel
from account import models as amod
from django.http import HttpResponse, HttpResponseRedirect
import decimal

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
	user = models.ForeignKey('account.FomoUser', on_delete=models.CASCADE, related_name="user_cart")
	product = models.ForeignKey('catalog.Product', null=True)
	quantity = models.IntegerField(default=1)
	date_added = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(auto_now=True)
	tax = models.DecimalField(max_digits=8, decimal_places=4, default=.0725)
	total_shipping = models.DecimalField(max_digits=8, decimal_places=2, default=10)
	sold = models.BooleanField(default=False)
	active = models.BooleanField(default=True)

	# Convienence Methods -- Test Still

	# remove item from cart
	@staticmethod
	def remove_item(pid, uid):
		cart = ShoppingCart.objects.filter(user_id=uid)
		cart = cart.filter(sold=False)
		cart = cart.filter(active=True)
		cart = cart.filter(product_id=pid)
		for c in cart:
			if hasattr(c.product, 'quantity'):
				c.product.quantity += c.quantity
				c.product.save()
			if hasattr(c.product, 'available'):
				c.product.available = True
				c.product.save()
			c.active = False
			c.save()
		return 4

	# clear cart
	@staticmethod
	def clear_cart(user_id):
		cart = ShoppingCart.objects.filter(user_id=user_id)
		cart = cart.filter(sold=False)
		cart = cart.filter(active=True)
		for c in cart:
			if hasattr(c.product, 'quantity'):
				c.product.quantity += c.quantity
				c.product.save()
			if hasattr(c.product, 'available'):
				c.product.available = True
				c.product.save()
			c.active = False
			c.save()
		return 4
        
	# Retrieve Items --> In FomoUser class

	# Calculate Subtotal
	@staticmethod
	def calc_subtotal(user_id):
		cart = ShoppingCart.objects.filter(user_id=user_id)
		cart = cart.filter(sold=False)
		cart = cart.filter(active=True)
		total = 0
		for c in cart:
				total += (c.product.price*c.quantity)
		return decimal.Decimal(total)

	@staticmethod
	def calc_tax(subtotal):
		return decimal.Decimal(subtotal*ShoppingCart.objects.get(id=1).tax)

	@staticmethod
	def calc_total_amount(user_id):
		cart = ShoppingCart.objects.filter(user_id=user_id)
		cart = cart.filter(sold=False)
		cart = cart.filter(active=True)
		total = 0
		for c in cart:
				total += (c.product.price*c.quantity)

		return decimal.Decimal(total+(total*ShoppingCart.objects.get(id=1).tax))


		


	# Number of items in cart --> In FomoUser class

class Sale(models.Model):
	user = models.ForeignKey('account.FomoUser', related_name="user_sales")
	sale_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(auto_now=True)
	sale_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
	total_tax = models.DecimalField(max_digits=8, decimal_places=2, default=0)

	# Convienence Method

	@staticmethod
	def record_sale(user, cart_items_list, address, city, state, zipcode, stripe_charge_token):

		# call stripe API, pass the token, and see if it returns true or false stripeResponse = 

		# this if statement would check to see if the token is valid at stripe
		# if stripe_charge_token:
			# If the stripe API returns true

		sale = Sale()
		sale.user = user
		sale.sale_price = ShoppingCart.calc_subtotal(user.id)
		sale.save()

		# try:

		for item in cart_items_list:
			sale_item = SaleItem()
			sale_item.sale = sale
			sale_item.product = item.product
			sale_item.quantity = item.quantity
			sale_item.sale_price = item.product.price
			sale_item.tax_amount = ShoppingCart.calc_tax(sale_item.sale_price)
			# sale_item.discount = item.discount
			sale_item.save()
			sale.sale_price = sale.sale_price + sale_item.sale_price
			sale.total_tax = ShoppingCart.calc_tax(sale.sale_price)
			# if hasattr(item.product, 'quantity'):
			# 	item.product.quantity -= item.quantity
			if hasattr(item.product, 'sold'):
				item.product.sold = True

			item.product.save()

		payment = Payment()
		payment.sale = sale
		payment.total_paid = sale.sale_price
		payment.save()

		sale.save()

		shipping = amod.ShippingAddress()
		shipping.shipping_address = address
		shipping.shipping_city = city
		shipping.shipping_state = state
		shipping.shipping_zipcode = zipcode
		shipping.user = user

		shipping.save()

		# except BaseException:
		# 	return False

		return 4

		# Returns false if stripe returned false
		# return False


	# Convienence Methods

class SaleItem(models.Model):
	sale = models.ForeignKey('Sale', on_delete=models.CASCADE, related_name='sale')
	product = models.ForeignKey('Product', related_name='saleitems', null=True)
	sale_price = models.DecimalField(max_digits=8, decimal_places=2)
	discount = models.DecimalField(max_digits=8, decimal_places=2, null=True)
	tax = models.DecimalField(max_digits=8, decimal_places=4, default=.0725)
	tax_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
	quantity = models.IntegerField(default=1)

	# Convienence Methods

	# Calc Price
	def calc_sale_price(self):
		self.sale_price = self.product.price*self.quantity
		return decimal.Decimal(self.sale_price)

	# Calc Tax
	def calc_tax_amount(self):
		self.tax_amount = self.sale_price * self.tax
		return self.tax_amount

	# Calc total price
	def calc_total_price(self):
		return decimal.Decimal((self.sale_price+self.tax_amount))

class Payment(models.Model):
	sale = models.ForeignKey('Sale', on_delete=models.CASCADE, related_name='payments')
	total_paid = models.DecimalField(max_digits=8, decimal_places=2)
	payment_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(auto_now=True)

	# Convienence Methods














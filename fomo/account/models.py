from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Sum

from catalog import models as cmod


# The models for the Account application


## Model for Fomo's Users
class FomoUser(AbstractUser):

	###The fields commented below are inherited from the AbstractBaseUsser and AbstractUser classes

    # username
    # first_name
    # last_name
    # password
    # email
    # last_login

    #Gender Types

    GENDER_CHOICES = (
    	('male', 'Male'),
    	('female', 'Female'),
    	('other', 'Other'),
    )
        
    birth_date = models.DateTimeField('Birth Date')
    gender = models.TextField(null=True, blank=True, choices=GENDER_CHOICES, default = 'other',)

    def get_cart_count(self):
        cart = cmod.ShoppingCart.objects.filter(user_id=self.id)
        cart = cart.filter(sold=False)
        cart = cart.filter(active=True)
        qty = 0
        for c in cart:
            qty = qty + c.quantity
        return qty

    # Don't for get to test the following

    def get_cart(self):
        cart = cmod.ShoppingCart.objects.filter(user_id=self.id)
        cart = cart.filter(sold=False)
        cart = cart.filter(active=True)
        return cart

    def cart_total(self):
        cart = cmod.ShoppingCart.objects.filter(user_id=self.id)
        cart = cart.filter(sold=False)
        cart = cart.filter(active=True)
        total = 0
        for c in cart:
            total += (c.product.price*c.quantity)
        tax = total*cmod.ShoppingCart.objects.get(id=1).tax
        total = total+tax
        total = (total+10)*100
        return round(total,2)


class ShippingAddress(models.Model):
    user = models.ForeignKey('account.FomoUser', related_name="sales")
    shipping_address = models.TextField()
    shipping_city = models.TextField()
    shipping_state = models.TextField()
    shipping_zipcode = models.TextField()




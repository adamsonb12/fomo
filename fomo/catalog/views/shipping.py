from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django_mako_plus import view_function
from datetime import datetime
from catalog import models as cmod
from account import models as amod
from .. import dmp_render, dmp_render_to_string
import json as json
from django.contrib.auth.decorators import login_required
import requests
import stripe
import decimal

from formlib.form import FormMixIn
from django import forms


@view_function
@login_required()
def process_request(request):

	uid = request.user.id

	try:
		user = amod.FomoUser.objects.get(id=uid)
		cart = cmod.ShoppingCart.objects.filter(user_id=uid)
	except cmod.ShoppingCart.DoesNotExist:
		return HttpResponseRedirect('/catalog/index')

	form = ShippingForm(request, user=user)
	if form.is_valid():
		form.commit(user=user)
			# sale = cmod.Sale.objects.filter(user_id=uid)
			# sale = sale.get(user_id=uid)
			# print('>>>>>>>>>>>>>>>>>>>>>>', sale.id)
		return HttpResponseRedirect('/catalog/receipt/1')
		

	subtotal = cmod.ShoppingCart.calc_subtotal(uid) 
	tax = cmod.ShoppingCart.calc_tax(subtotal)
	shipping = cart[0].total_shipping
	total = subtotal + tax + shipping
	
	context = {
		'user': user,
		'form': form,
		'subtotal': subtotal,
		'tax': tax,
		'shipping': shipping,
		'total': total,
	}

	return dmp_render(request, 'shipping.html', context)

# Make this into a Form crap
class ShippingForm(FormMixIn, forms.Form):

	form_submit = 'Submit Address & Continue to Payment'
	form_id = 'shipping_form'
	
	def init(self, user):

		self.fields['name'] = forms.CharField(label='Addressed to', required=True)
		self.fields['address'] = forms.CharField(label='Address', required=True)
		self.fields['city'] = forms.CharField(label='City', required=True)
		self.fields['state'] = forms.ChoiceField(label='State', choices=[
			['AL', 'Alabama'], ['AZ', 'Arizona'], ['AR', 'Arkansas'], ['CA', 'California'], ['CO', 'Colorado'], ['CT', 'Connecticut'], ['DE', 'Delaware'], ['DC', 'District of Columbia'], ['FL', 'Florida'], ['GA', 'Georgia'], ['ID', 'Idaho'], ['IL', 'Illinois'], ['IN', 'Indiana'], ['IA', 'Iowa'], ['KS', 'Kansas'], ['KY', 'Kentucky'], ['LA', 'Louisiana'], ['ME', 'Maine'], ['MD', 'Maryland'], ['MA', 'Massachusetts'], ['MI', 'Michigan'], ['MN', 'Minnesota'], ['MS', 'Mississippi'], ['MO', 'Missouri'], ['MT', 'Montana'], ['NE', 'Nebraska'], ['NV', 'Nevada'], ['NH', 'New Hampshire'], ['NJ', 'New Jersey'], ['NM', 'New Mexico'], ['NY', 'New York'], ['NC', 'North Carolina'], ['ND', 'North Dakota'], ['OH', 'Ohio'], ['OK', 'Oklahoma'], ['OR', 'Oregon'], ['PA', 'Pennsylvania'], ['RI', 'Rhode Island'], ['SC', 'South Carolina'], ['SD', 'South Dakota'], ['TN', 'Tennessee'], ['TX', 'Texas'], ['UT', 'Utah'], ['VT', 'Vermont'], ['VA', 'Virginia'], ['WA', 'Washington'], ['WV', 'West Virginia'], ['WI', 'Wisconsin'], ['WY', 'Wyoming']
			])
		self.fields['zipcode'] = forms.CharField(label='Zipcode', required=True)
		self.fields['stripe_token'] = forms.CharField(required=False, widget=forms.HiddenInput())

	def clean(self):
		# get their data
		self.data = self.data.copy()
		address = self.cleaned_data.get('address')
		city = self.cleaned_data.get('city')
		state = self.cleaned_data.get('state')
		zipcode = self.cleaned_data.get('zipcode')

		# verify with googles api
		response = requests.get('https://maps.googleapis.com/maps/api/geocode/json', params = { 'address': address + ' ' + city + ', ' + state + ' ' + zipcode, 'key': 'AIzaSyB5e7VTwO-PMxVoJV_eSwCZEa1d7S5VhQE'})
		response = response.json()
		for t in response['results'][0]['address_components']:
			if 'subpremise' in t['types']:
				google_apt = t['long_name']
				google_apt = ' #' + google_apt
			if 'street_number' in t['types']:
				google_street = t['long_name']
			if 'route' in t['types']:
				google_route = t['long_name']
			if 'locality' in t['types']:
				google_city = t['long_name']
			if 'administrative_area_level_1' in t['types']:
				google_state = t['long_name']
			if 'postal_code' in t['types']:
				google_zipcode = t['long_name']

		# save over their data
		changed = False
		if self.data['address'] != google_street + ' ' + google_route:
			self.data['address'] = google_street + ' ' + google_route
			changed = True
		if self.data['city'] != google_city:
			self.data['city'] = google_city
			changed = True
		# self.data['state'] = google_state
		if self.data['zipcode'] != google_zipcode:
			self.data['zipcode'] = google_zipcode
			changed = True
		if changed:
			raise forms.ValidationError('Will this address work?')

		return self.data

	def commit(self, user):
		self.user = user
		ship = amod.ShippingAddress()
		ship.user = self.user
		ship.shipping_address = self.cleaned_data.get('address')
		ship.shipping_city = self.cleaned_data.get('city')
		ship.shipping_state = self.cleaned_data.get('state')
		ship.shipping_zipcode = self.cleaned_data.get('zipcode')
		ship.save()

		# Charge the user's card:
		stripe.api_key = 'sk_test_GSBjiFPDdOSeRPVP9ZifNmb9'
		charge = stripe.Charge.create(
		  amount=self.user.cart_total(),
		  currency="usd",
		  description="Example charge",
		  source= self.cleaned_data.get('stripe_token')
		)

		# record sale 
		sale = cmod.Sale()
		sale.user = user
		sale.sale_price = cmod.ShoppingCart.calc_subtotal(user.id)
		sale.save()

		# sale item objects
		cart = self.user.get_cart()
		for c in cart:
			item = cmod.SaleItem()
			item.sale = sale
			item.product = c.product
			item.quantity = c.quantity
			item.sale_price = item.calc_sale_price()
			item.tax_amount = 5
			item.save()

		# sale receipt thing

		#clear cart
		for c in cart:
			if hasattr(c.product, 'sold'):
				c.sold = True
				c.save()
				c.product.sold = True
				c.product.save()

		return 4



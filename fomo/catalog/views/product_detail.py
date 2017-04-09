from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django_mako_plus import view_function
from datetime import datetime
from catalog import models as cmod
from account import models as amod
from .. import dmp_render, dmp_render_to_string
import json as json
import random 

from formlib.form import FormMixIn
from django import forms

@view_function
def process_request(request):

	try: 
		product = cmod.Product.objects.get(id=request.urlparams[0])
		jsonDec = json.decoder.JSONDecoder()
		dList = jsonDec.decode(product.descriptionList)
		iList = jsonDec.decode(product.imgList)
		user = amod.FomoUser.objects.get(id=request.user.id)
	except cmod.Product.DoesNotExist:
		return HttpResponseRedirect('/manager/products/')

	# Add to last five -> actually product history
	new_prod = cmod.ProductHistory()
	new_prod.user = user
	new_prod.product = product
	new_prod.save()

	form = AddToCartForm(request, product=product)
	if form.is_valid():
		form.commit()

	template = 'product_detail.html'
	if request.method == 'POST':
		template = 'product_detail_ajax.html'

	context = {
	    'product': product,
	    'dList': dList,
	    'iList': iList,
	    'form': form,
	}
	return dmp_render(request, template, context)

# Make this into a Form crap
class AddToCartForm(FormMixIn, forms.Form):

	form_submit = 'Add to Cart'
	form_id = 'add_to_cart_form'
	
	def init(self, product):

		self.product = product

		if hasattr(product, 'quantity'):
			self.fields['quantity'] = forms.IntegerField(required=False)
 
	# Clean method here
	def clean_quantity(self):
		qty = self.cleaned_data.get('quantity')
		if self.product.quantity < qty:
			raise forms.ValidationError('''Sorry! We don't have that much in stock. ''')
		return qty

	def commit(self):

		try:
			user = amod.FomoUser.objects.get(id=self.request.user.id)
		except amod.FomoUser.DoesNotExist:
			return HttpResponseRedirect('/catalog/index')

		cart = cmod.ShoppingCart()
		cart.user = user
		cart.product = self.product

		qty = self.cleaned_data.get('quantity')

		# check product availability 
		if hasattr(cart.product, 'quantity'):
			cart.quantity = qty
			self.product.quantity -= qty
			self.product.save()
		if hasattr(cart.product, 'available'):
			if self.product.available == True:
				self.product.available = False
				self.product.save()
			else:
				raise forms.ValidationError(''' Sorry! That product is no longer available ''')
		cart.save()
		# ret = stripe charge token
		return 4
		
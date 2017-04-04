from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django_mako_plus import view_function
from datetime import datetime
from catalog import models as cmod
from .. import dmp_render, dmp_render_to_string
import json as json

from formlib.form import FormMixIn
from django import forms

@view_function
def process_request(request):

	try: 
		product = cmod.Product.objects.get(id=request.urlparams[0])
		jsonDec = json.decoder.JSONDecoder()
		dList = jsonDec.decode(product.descriptionList)
		iList = jsonDec.decode(product.imgList)
	except cmod.Product.DoesNotExist:
		return HttpResponseRedirect('/manager/products/')

	# Add to last five
	for l in request.last5:
		if(product.id == l):
			request.last5.remove(product.id)
	request.last5.insert(0, product.id)

	form = AddToCartForm(request, product=product)
	if form.is_valid():
		form.commit()

	context = {
	    'product': product,
	    'dList': dList,
	    'iList': iList,
	    'form': form,
	}
	return dmp_render(request, 'product_detail.html', context)

# Make this into a Form crap
class AddToCartForm(FormMixIn, forms.Form):

	form_submit = 'Add to Cart'
	form_id = 'add_to_cart_form'
	
	def init(self, product):

		if hasattr(product, 'quantity'):
			self.fields['quantity'] = forms.IntegerField(required=False)

	# Clean method here
	def clean_quantity(self):
		qty = self.cleaned_data.get('quantity')
		# Call database
			# raise form.ValidationError('''Sorry! We don't have that much in stock. ''')
		return qty

	def commit(self):
		pass

# @view_function
# def add_to_cart(request):

# 	uid = request.user.id
# 	pid = request.urlparams[0]
# 	quantity = 1
# 	cmod.ShoppingCart.addItem(uid, pid, quantity)
# 	return HttpResponseRedirect('/catalog/product_detail/' + pid)

# 	# add item to cart
# 	def addItem(uid, pid, quantity):
# 		try:
# 			user = amod.objects.get(id=uid)
# 			product = Product.objects.get(id=pid)
# 		except:
# 			return HttpResponseRedirect('/catalog/index/')

# 		cart = ShoppingCart()
# 		cart.user = user
# 		cart.product = product

# 		# check product availability 
# 		if hasattr(product, 'quantity'):
# 			if product.quantity < quantity:
# 				return HttpResponse('Not enough in Inventory')
# 			cart.product.quantity = quantity
# 			product.quantity -= quantity
# 			product.save()
# 		if hasattr(product, 'available'):
# 			if product.available:
# 				product.available = False
# 				product.save()
# 			else:
# 				return HttpResponse('Product No Longer Available')
# 		cart.save()
# 		return 4
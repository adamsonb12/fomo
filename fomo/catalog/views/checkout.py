from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django_mako_plus import view_function
from datetime import datetime
from catalog import models as cmod
from .. import dmp_render, dmp_render_to_string
import json as json
from django.contrib.auth.decorators import login_required


@view_function
@login_required()
def process_request(request):

	uid = request.user.id

	try:
		cart = cmod.ShoppingCart.objects.filter(user_id=uid)
	except cmod.Category.DoesNotExist:
		return HttpResponseRedirect('/homepage/')

	subtotal = cmod.ShoppingCart.calc_subtotal(uid) 
	tax = cmod.ShoppingCart.calc_tax(subtotal)
	shipping = cart[0].total_shipping
	total = subtotal + tax + shipping
	
	context = {
		'cart': cart,
		'uid': uid,
		'subtotal': subtotal,
		'tax': tax,
		'shipping': shipping,
		'total': total,
	}

	return dmp_render(request, 'checkout.html', context)


@view_function
@login_required()
def clear_cart(request):
	cmod.ShoppingCart.clear_cart(request.user.id)
	return HttpResponseRedirect('/catalog/checkout')

@view_function
@login_required()
def remove_item(request):
	uid = request.user.id
	prod = request.GET.get('product')
	cmod.ShoppingCart.remove_item(prod, uid)
	return HttpResponseRedirect('/catalog/checkout')
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseNotFound
from django_mako_plus import view_function
from django.contrib.auth import authenticate, login
from .. import dmp_render, dmp_render_to_string
from django import forms

from formlib.form import FormMixIn
from catalog import models as cmod
import json


@view_function
def process_request(request):

	product_name = request.GET.get('prod_name')
	min_price = request.GET.get('min_price')
	max_price = request.GET.get('max_price')
	category_name = request.GET.get('category')

	products = []
	qry = cmod.Product.objects

	if product_name:
		qry = qry.filter(name__icontains=product_name)
	if min_price:
		qry = qry.filter(price__gte=min_price)
	if max_price:
		qry = qry.filter(price__lte=max_price)
	if category_name:
		qry = qry.filter(category__name__icontains=category_name)

	if qry.exists():
		for p in qry:
			if hasattr(p, 'serial_number'):
				ret = { 
				'name': p.name,
				'serial_number': p.serial_number,
				'category': p.category.name,
				'price': p.price,
				}

			if hasattr(p, 'quantity'):
				ret = { 
				'name': p.name,
				'quantity': p.quantity,
				'category': p.category.name,
				'price': p.price,
				}
			products.append(ret)
	else:
		return HttpResponseNotFound('Incorrect Query')

	return JsonResponse(products, safe=False)
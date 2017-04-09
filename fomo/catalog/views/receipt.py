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

from formlib.form import FormMixIn
from django import forms


@view_function
@login_required()
def process_request(request):

	try:
		sale = cmod.Sale.objects.get(id=request.urlparams[0])
		items = cmod.SaleItem.objects.filter(sale_id=sale.id)
	except cmod.ShoppingCart.DoesNotExist:
		return HttpResponseRedirect('/catalog/index')
	
	context = {
		'sale': sale,
		'items': items,
	}

	return dmp_render(request, 'receipt.html', context)
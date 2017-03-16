from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django_mako_plus import view_function
from datetime import datetime
from catalog import models as cmod
from .. import dmp_render, dmp_render_to_string
import json as json

@view_function
def process_request(request):

	try:
		categories = cmod.Category.objects.filter()
		products = cmod.Product.objects.filter()
	except cmod.Category.DoesNotExist:
		return HttpResponseRedirect('/homepage/')

	context = {
		'categories': categories,
		'products': products,
	}


	return dmp_render(request, 'index.html', context)
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
		if(request.urlparams[0] == None or request.urlparams[0] == ''):
			products = cmod.Product.objects.all()
		else:
			products = cmod.Product.objects.filter(category = request.urlparams[0])

	except cmod.Category.DoesNotExist:
		return HttpResponseRedirect('/homepage/')
	
	

	context = {
		'categories': categories,
		'products': products,
	}


	return dmp_render(request, 'index.html', context)
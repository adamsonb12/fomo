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
		products = cmod.ShoppingCart.objects.filter(id=uid)
	except cmod.Category.DoesNotExist:
		return HttpResponseRedirect('/homepage/')
	
	

	context = {
		'products': products,
	}


	return dmp_render(request, 'checkout.html', context)
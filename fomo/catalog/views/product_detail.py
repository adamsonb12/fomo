from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django_mako_plus import view_function
from datetime import datetime
from catalog import models as cmod
from .. import dmp_render, dmp_render_to_string

@view_function
def process_request(request):

	try: 
		product = cmod.Product.objects.get(id=request.urlparams[0])
	except cmod.Product.DoesNotExist:
		return HttpResponseRedirect('/manager/products/')

	context = {
	    'product': product,
	}
	return dmp_render(request, 'product_detail.html', context)
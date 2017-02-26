from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django_mako_plus import view_function
from datetime import datetime
from catalog import models as cmod
from .. import dmp_render, dmp_render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

@view_function
@login_required()
@permission_required('add_fomouser')
def process_request(request):

	# Query to display all products
	products = cmod.Product.objects.order_by('name').all()


	context = {   
		'products': products, 
	}
	return dmp_render(request, 'products.html', context)


@view_function
def get_quantity(request):
	# gets the current quantity of product id in urlparams[0]

	try: 
		product = cmod.BulkProduct.objects.get(id=request.urlparams[0])
	except cmod.BulkProduct.DoesNotExist:
		return HttpResponseRedirect('/manager/products/')

	return HttpResponse(product.quantity)
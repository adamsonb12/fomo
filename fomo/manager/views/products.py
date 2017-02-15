from django.conf import settings
from django_mako_plus import view_function
from datetime import datetime
from catalog import models as cmod
from .. import dmp_render, dmp_render_to_string

@view_function
def process_request(request):

	# Query to display all products
	products = cmod.Product.objects.order_by('name').all()


    context = {   
    	'products': products, 
    }
    return dmp_render(request, 'products.html', context)
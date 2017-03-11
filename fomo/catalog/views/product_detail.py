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
		add = True
		product = cmod.Product.objects.get(id=request.urlparams[0])
		jsonDec = json.decoder.JSONDecoder()
		dList = jsonDec.decode(product.descriptionList)
		iList = jsonDec.decode(product.imgList)
	except cmod.Product.DoesNotExist:
		return HttpResponseRedirect('/manager/products/')

	# Add to last five
	for l in request.last5:
		if(product.id == l):
			add = False
	if(add == True):
		request.last5.insert( 0, product.id)

	context = {
	    'product': product,
	    'dList': dList,
	    'iList': iList,
	}
	return dmp_render(request, 'product_detail.html', context)
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django_mako_plus import view_function
from datetime import datetime
from catalog import models as cmod
from .. import dmp_render, dmp_render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Permission, Group

@view_function
def process_request(request):

	# Query to display all products
	permissions = Permission.objects.order_by('name').all()


	context = {   
		'permissions': permissions, 
	}
	return dmp_render(request, 'permissions.html', context)
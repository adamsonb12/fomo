from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django_mako_plus import view_function
from datetime import datetime
from account import models as amod
from .. import dmp_render, dmp_render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Permission, Group

@view_function
def process_request(request):

	# Query to display all products
	permissions = amod.FomoUser.objects.get(id=request.urlparams[0]).permissions


	context = {   
		'permissions': permissions, 
	}
	return dmp_render(request, 'permissionslist.html', context)
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django_mako_plus import view_function
from datetime import datetime
from account import models as amod
from .. import dmp_render, dmp_render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

@view_function
@login_required()
@permission_required('add_fomouser')
def process_request(request):

	# Query to display all users
	users = amod.FomoUser.objects.order_by('last_name').all()


	context = {   
		'users': users, 
	}
	return dmp_render(request, 'users.html', context)
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
@permission_required('change_fomouser')
def process_request(request):

	uid = request.user.id

	try: 
		user = amod.FomoUser.objects.get(id=uid)
	except amod.FomoUser.DoesNotExist:
		return HttpResponseRedirect('/manager/products/')

	context = {
    	'user': user,
	}
	return dmp_render(request, 'account_info.html', context)
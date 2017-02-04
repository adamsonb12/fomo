from django.conf import settings
from django.http import HttpResponseRedirect
from django_mako_plus import view_function
from django.contrib.auth import authenticate, login

@view_function
def process_request(request):
	#authenticate the user
	username = 'user1'
	password = 'password'

	user = authenticate(username=username, password=password)
	if user is not None:
	    login(request,user)

		# return HttpResponseRedirect('/account/index/')

	# return HttpResponseRedirect('/')

	return HttpResponseRedirect('/account/index')
	    
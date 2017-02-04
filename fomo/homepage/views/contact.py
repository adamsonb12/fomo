from django.conf import settings
from django_mako_plus import view_function
from .. import dmp_render, dmp_render_to_string

@view_function
def process_request(request):

	print('>>>>>', request.GET.get('namefull'))
	print('>>>>>', request.GET.get('useremail'))
	print('>>>>>', request.GET.get('emailsubject'))
	print('>>>>>', request.GET.get('emailmessage'))

	return dmp_render(request, 'contact.html', {})
	
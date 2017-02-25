from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django_mako_plus import view_function
from django.contrib.auth import authenticate, login
from datetime import datetime
from account import models as amod
from .. import dmp_render, dmp_render_to_string
from formlib.form import FormMixIn
from django import forms

@view_function
def process_request(request):

    # process the form
	form = LoginForm(request)
	if form.is_valid():
	    form.commit()
	    return HttpResponseRedirect('/manager/users/')

	context = {
	    'form': form,
	}
	return dmp_render(request, 'login.html', context)

class LoginForm(FormMixIn, forms.Form):
	
	def init(self):
	    self.fields['username'] = forms.CharField(label='Username', max_length=100)
	    self.fields['password'] = forms.CharField(label='Password', max_length=100)

	def commit(self):

		un = self.cleaned_data.get('username')
		ps = self.cleaned_data.get('password')

		user = authenticate(username=un, password=ps)
		if user is not None:
			login(request, user)
			return HttpResponseRedirect('/manager/users')
		else:
			return HttpResponseRedirect('/')









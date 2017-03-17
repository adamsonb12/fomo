from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django_mako_plus import view_function
from django.contrib.auth import authenticate, login
from .. import dmp_render, dmp_render_to_string
from django import forms

from formlib.form import FormMixIn
from account import models as amod


@view_function
def process_request(request):

    # process the form
	form = LoginForm(request)
	if form.is_valid():
	    form.commit(request)
	    return HttpResponseRedirect('/account/account_info/')

	return dmp_render(request, 'login.html', {
		'form': form,
		})

class LoginForm(FormMixIn, forms.Form):
	
	def init(self):
		self.form_action = '/account/login.modal/'
		self.fields['username'] = forms.CharField(required=True)
		self.fields['password'] = forms.CharField(required=True, widget=forms.PasswordInput())

	def clean(self):
		self.user = authenticate(username=self.cleaned_data.get('username'), password=self.cleaned_data.get('password'))
		if self.user is None:
			raise forms.ValidationError('Invalid username or password')
		return self.cleaned_data

	def commit(self, request):
		login(request, self.user)
		return 4

@view_function
def modal(request):

    # process the form
	form = LoginForm(request)
	if form.is_valid():
	    form.commit(request)
	    return HttpResponseRedirect('/account/account_info/')

	return dmp_render(request, 'login.modal.html', {
		'form': form,
		})










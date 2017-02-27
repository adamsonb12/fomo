from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django_mako_plus import view_function
from datetime import datetime
from account import models as amod
from .. import dmp_render, dmp_render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

from formlib.form import FormMixIn
from django import forms

@view_function
@login_required()
@permission_required('change_fomouser')
def process_request(request):

	try: 
		user = amod.FomoUser.objects.get(id=request.urlparams[0])
	except amod.FomoUser.DoesNotExist:
		return HttpResponseRedirect('/account/account_info/')

	# process the form
	form = PasswordChangeForm(request, user=user)
	if form.is_valid():
	    form.commit(user)
	    return HttpResponseRedirect('/')

	context = {
	    'user': user,
	    'form': form,
	}
	return dmp_render(request, 'password.html', context)


class PasswordChangeForm(FormMixIn, forms.Form):
	
	def init(self, user):
	    self.fields['current_password'] = forms.CharField(label='Current Password', max_length=100, widget=forms.PasswordInput())
	    self.fields['new_password'] = forms.CharField(label='New Password', max_length=100, widget=forms.PasswordInput())
	    self.fields['confirm'] = forms.CharField(label='Confirm New Password', max_length=100, widget=forms.PasswordInput())

	

	def commit(self, user):

		## test old password
		old = self.cleaned_data.get('current_password')

		if user.check_password(old) == False:
			raise forms.ValidationError('Incorrect password')

		## Make sure both new passwords match

		if self.cleaned_data.get('new_password') != self.cleaned_data.get('confirm'):
			raise forms.ValidationError("The passwords don't match")

		user.set_password(self.cleaned_data.get('new_password'))
		user.save()
		return 4








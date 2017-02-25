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
@permission_required('add_fomouser')
def process_request(request):

	# process the form
	form = UserCreateForm(request)
	if form.is_valid():
	    form.commit()
	    return HttpResponseRedirect('/manager/users/')

	context = {
	    'form': form,
	}
	return dmp_render(request, 'create_user.html', context)


class UserCreateForm(FormMixIn, forms.Form):
	
	def init(self, user):
	    self.fields['first_name'] = forms.CharField(label='First Name', max_length=100)
	    self.fields['last_name'] = forms.CharField(label='Last Name', max_length=100)
	    self.fields['username'] = forms.CharField(label='Username', max_length=100)
	    self.fields['email'] = forms.CharField(label='Email Address', max_length=100)
	    self.fields['birth_date'] = forms.CharField(label='Birth Date', max_length=100)
	    self.fields['gender'] = forms.ChoiceField(label='Gender', choices=[
			['male', 'Male'],
			['female', 'Female'],
			['other', 'Other'],
			])

	def commit(self):

		## see if the new username is uniqu
		un = self.cleaned_data.get('username')
		users = amod.FomoUser.objects.filter(username=un)

		if len(users) > 0:
			raise forms.ValidationError(
				"That username has already been taken, please choose a different one")
		else:

			user = amod.FomoUser()

			user.first_name = self.cleaned_data.get('first_name')
			user.last_name = self.cleaned_data.get('last_name')
			user.username = self.cleaned_data.get('username')
			user.email = self.cleaned_data.get('email')
			user.birth_date = self.cleaned_data.get('birth_date')
			user.gender = self.cleaned_data.get('gender')
			
			user.save()
			return 4





from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django_mako_plus import view_function
from datetime import datetime
from account import models as amod
from .. import dmp_render, dmp_render_to_string
from formlib.form import FormMixIn
from django import forms

@view_function
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

		# if ():## see if the username has already been used

		# else:
			## display an error message about changing their username

		user = amod.FomoUser()

		user.first_name = self.cleaned_data.get('first_name')
		user.last_name = self.cleaned_data.get('last_name')
		user.username = self.cleaned_data.get('username')
		user.email = self.cleaned_data.get('email')
		user.birth_date = self.cleaned_data.get('birth_date')
		user.gender = self.cleaned_data.get('gender')
		
		user.save()
		return 4





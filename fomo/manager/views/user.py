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

	try: 
		user = amod.FomoUser.objects.get(id=request.urlparams[0])
	except amod.FomoUser.DoesNotExist:
		return HttpResponseRedirect('/manager/users/')

	# process the form
	form = UserEditForm(request, user=user, initial={
		'first_name': user.first_name,
		'last_name': user.last_name,
		'username': user.username,
		'email': user.email,
		'birth_date': user.birth_date,
		'gender': user.gender,
		})
	if form.is_valid():
	    form.commit(user)
	    return HttpResponseRedirect('/manager/users/')

	context = {
	    'user': user,
	    'form': form,
	}
	return dmp_render(request, 'user.html', context)


class UserEditForm(FormMixIn, forms.Form):
	
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

	def commit(self, user):
		user.first_name = self.cleaned_data.get('first_name')
		user.last_name = self.cleaned_data.get('last_name')
		## Logic here to make sure that the username isn't already taken
		user.username = self.cleaned_data.get('username')
		user.email = self.cleaned_data.get('email')
		user.birth_date = self.cleaned_data.get('birth_date')
		user.gender = self.cleaned_data.get('gender')
		user.save()


#######################################################################

## Delete a User

@view_function
def delete(request):

	try: 
		user = amod.FomoUser.objects.get(id=request.urlparams[0])
	except amod.FomoUser.DoesNotExist:
		return HttpResponseRedirect('/manager/users/')

	user.delete()
	return HttpResponseRedirect('/manager/users/')





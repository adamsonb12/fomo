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

		## see if the new username is uniqu
		un = self.cleaned_data.get('username')
		users = amod.FomoUser.objects.filter(username=un).exclude(id=user.id )

		if len(users) > 0:
			raise forms.ValidationError(
				"That username has already been taken, please choose a different one")
		else:

			user.first_name = self.cleaned_data.get('first_name')
			user.last_name = self.cleaned_data.get('last_name')
			user.username = self.cleaned_data.get('username')
			user.email = self.cleaned_data.get('email')
			user.birth_date = self.cleaned_data.get('birth_date')
			user.gender = self.cleaned_data.get('gender')
			user.save()


#######################################################################

## Delete a User

@view_function
@permission_required('delete_fomouser')
def delete(request):

	try: 
		user = amod.FomoUser.objects.get(id=request.urlparams[0])
	except amod.FomoUser.DoesNotExist:
		return HttpResponseRedirect('/manager/users/')

	user.delete()
	return HttpResponseRedirect('/manager/users/')





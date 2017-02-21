from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django_mako_plus import view_function
from datetime import datetime
from catalog import models as cmod
from .. import dmp_render, dmp_render_to_string
from formlib.form import FormMixIn
from django import forms

@view_function
def process_request(request):

	# print('>>>>>', request.GET.get('namefull'))
	# print('>>>>>', request.GET.get('useremail'))
	# print('>>>>>', request.GET.get('emailsubject'))
	# print('>>>>>', request.GET.get('emailmessage'))

	# if request.method == 'POST':
	# 	print('-----------POSTED')
	# 	form = ContactForm(request.POST)
	# 	if form.is_valid():
	# 	# act on the form here
	# 		print('----------VALID')
	# 		return HttpResponseRedirect('/')

	form = ContactForm(request)

	return dmp_render(request, 'contact.html', {
		'form': form,
		})

class ContactForm(FormMixIn, forms.Form):
    # name = forms.CharField(label='Full Name', max_length=100)
    # email = forms.EmailField(label='Email', max_length=100)
    # message = forms.CharField(label='Message', max_length=1000)
		# widget = forms.TextArea(attrs={'class': 'form-control'})

	def init(self):
		self.fields['name'] = forms.CharField(label='Full Name', max_length=100)
		self.fields['contactType'] = forms.ChoiceField(label='How should we contact you?', choices=[
			['phone', 'Phone Number'],
			['email', 'Email'],
			], widget=forms.RadioSelect())
		self.fields['phone'] = forms.CharField(label='Phone Number', max_length=100)
		self.fields['cell'] = forms.CharField(label='Cell Phone', max_length=100)
		self.fields['email'] = forms.EmailField(label='Email', max_length=100)
		self.fields['subject'] = forms.CharField(label='Subject', max_length=100)
		self.fields['message'] = forms.CharField(label='Message', max_length=1000)

	def clean_name(self):
		name = self.cleaned_data.get('name')

		parts = name.split()
		if len(parts) <= 1:
			raise forms.ValidationError('Please enter both first and last name')

		return name

	def commit(self, a, b):
		pass
		# send the email








	
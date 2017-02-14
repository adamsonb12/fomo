from django.conf import settings
from django import forms
from django.http import HttpResponseRedirect
from django_mako_plus import view_function
from .. import dmp_render, dmp_render_to_string

@view_function
def process_request(request):

	# print('>>>>>', request.GET.get('namefull'))
	# print('>>>>>', request.GET.get('useremail'))
	# print('>>>>>', request.GET.get('emailsubject'))
	# print('>>>>>', request.GET.get('emailmessage'))

	if request.method == 'POST':
		print('-----------POSTED')
		form = ContactForm(request.POST)
		if form.is_valid():
		# act on the form here
			print('----------VALID')
			return HttpResponseRedirect('/')


	else:
		# prepare an empty form
		print('---------IDK')
		form = ContactForm()
	return dmp_render(request, 'contact.html', {
		'form': form,
		})

class ContactForm(forms.Form):
    name = forms.CharField(label='Full Name', max_length=100)
    email = forms.EmailField(label='Email', max_length=100)
    message = forms.CharField(label='Message', max_length=1000)
		# widget = forms.TextArea(attrs={'class': 'form-control'})

    def clean_name(self):
    	name = self.cleaned_data.get('name')
    	parts = name.strip().split()
    	if len(parts) <= 1:
    		raise forms.ValidationError('Please enter both first and last name')

    	return name
	
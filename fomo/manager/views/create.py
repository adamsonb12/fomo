from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django_mako_plus import view_function
from datetime import datetime
from catalog import models as cmod
from .. import dmp_render, dmp_render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

from formlib.form import FormMixIn
from django import forms

@view_function
@login_required()
@permission_required('add_fomouser')
def process_request(request):

	# try: 
	# 	product = cmod.Product.objects.get(id=request.urlparams[0])
	# except cmod.Product.DoesNotExist:
	# 	return HttpResponseRedirect('/manager/products/')

	# process the form
	form = ProductCreateForm(request)
	if form.is_valid():
	    form.commit()
	    return HttpResponseRedirect('/manager/products/')

	context = {
	    'form': form,
	}
	return dmp_render(request, 'create.html', context)


class ProductCreateForm(FormMixIn, forms.Form):
	
	def init(self, product):
		self.fields['name'] = forms.CharField(label='Product Name', max_length=100)
		self.fields['producttype'] = forms.ChoiceField(label='Product Type', choices=[
			['bulk', 'Bulk Product'],
			['unique', 'Unique Product'],
			['rental', 'Rental Product'],
			])
		self.fields['category'] = forms.ModelChoiceField(label='Category', queryset=cmod.Category.objects.order_by('name').all())
		self.fields['serial'] = forms.CharField(label='Serial Number', max_length=100, widget=forms.TextInput(attrs={'class':'producttype-unique'}), required=False)
		self.fields['price'] = forms.DecimalField(label='Price')
		self.fields['quantity'] = forms.IntegerField(label='Quantity', widget=forms.TextInput(attrs={'class':'producttype-bulk'}), required=False)
		self.fields['reorder-trigger'] = forms.IntegerField(label='Reorder Trigger Amount', widget=forms.TextInput(attrs={'class':'producttype-bulk'}), required=False)
		self.fields['reorder-quantity'] = forms.IntegerField(label='Amount to Reorder', widget=forms.TextInput(attrs={'class':'producttype-bulk'}), required=False)

	def commit(self):

		if (self.cleaned_data.get('producttype') ==  'unique'):
			product = cmod.UniqueProduct()
			product.serial_number = self.cleaned_data.get('serial')
		elif (self.cleaned_data.get('producttype') ==  'bulk'):
			product = cmod.BulkProduct()
			product.quantity = self.cleaned_data.get('quantity')
			product.reorder_trigger = self.cleaned_data.get('reorder-trigger')
			product.reorder_quantity = self.cleaned_data.get('reorder-quantity')
		else:
			product = cmod.RentalProduct()
			product.serial_number = self.cleaned_data.get('serial')

		product.name = self.cleaned_data.get('name')
		product.category = self.cleaned_data.get('category')
		product.price = self.cleaned_data.get('price')
		product.save()
		return 4







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
@permission_required('change_bulkproduct')
def process_request(request):

	try: 
		product = cmod.Product.objects.get(id=request.urlparams[0])
	except cmod.Product.DoesNotExist:
		return HttpResponseRedirect('/manager/products/')

	# process the form
	form = ProductEditForm(request, product=product, initial={
		'name': product.name,
		'category': product.category,
		'price': product.price,
		'quantity': getattr(product, 'quantity', 0),
		})
	if form.is_valid():
	    form.commit(product)
	    return HttpResponseRedirect('/manager/products/')

	context = {
	    'product': product,
	    'form': form,
	}
	return dmp_render(request, 'product.html', context)


class ProductEditForm(FormMixIn, forms.Form):
	
	def init(self, product):
	    self.fields['name'] = forms.CharField(label='Product Name', max_length=100)
	    self.fields['category'] = forms.ModelChoiceField(label='Category', queryset=cmod.Category.objects.order_by('name').all())
	    self.fields['price'] = forms.DecimalField(label='Price')
	    if hasattr(product, 'quantity'):
	    	self.fields['quantity'] = forms.DecimalField(label='Quantity')

	def commit(self, product):
		product.name = self.cleaned_data.get('name')
		product.category = self.cleaned_data.get('category')
		product.price = self.cleaned_data.get('price')
		if hasattr(product, 'quantity'):
			product.quantity = self.cleaned_data.get('quantity')
		product.save()


#######################################################################

## Delete a Product

@view_function
@permission_required('delete_bulkproduct')
@permission_required('delete_uniqueproduct')
@permission_required('delete_rentalproduct')
def delete(request):

	try: 
		product = cmod.Product.objects.get(id=request.urlparams[0])
	except cmod.Product.DoesNotExist:
		return HttpResponseRedirect('/manager/products/')

	product.delete()
	return HttpResponseRedirect('/manager/products/')




















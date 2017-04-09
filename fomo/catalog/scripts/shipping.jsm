$(function() {

	var handler = StripeCheckout.configure({
	  key: 'pk_test_qwlwIBYygWgAOXlTh5KSAOPD',
	  image: 'https://stripe.com/img/documentation/checkout/marketplace.png',
	  locale: 'auto',
	  token: function(token) {
	    $('#id_stripe_token').val(token.id);
	  }
	});

	$('#shipping_form').submit(function(e) {
	  // Open Checkout with further options:
	  if ($('#id_stripe_token').val() != '') {
	  	return;
	  }
	  handler.open({
	    name: 'Fomo',
	    description: 'Music Store',
	    amount: ${ request.user.cart_total() }
	  });
	  e.preventDefault();
	});

	// Close Checkout on page navigation:
	window.addEventListener('popstate', function() {
	  handler.close();
	});

});
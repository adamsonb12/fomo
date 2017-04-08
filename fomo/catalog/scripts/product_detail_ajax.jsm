$(function() {
	// update shopping cart counter
	$('#cart_counter').html('${request.user.get_cart_count()}');
});
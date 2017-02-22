

$(function() {
	var producttype = $(id_producttype);

	producttype.change(function() {
		var value = producttype.val();
		if(value == 'bulk') {
			$('.producttype-bulk').closest('p').show(1000);
		}
		else
		{
			$('.producttype-bulk').closest('p').hide(1000);
		}
	});
	producttype.change();

});
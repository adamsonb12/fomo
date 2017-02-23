
$(function(){

	$('.delete-btn').click(function(event){
		//cancel default behavior
		event.preventDefault();

		//Modal
		$('#deleteProductModal').modal({
			//no options
		});

		var href = $(this).attr('href');
		$('#delete-confirm').attr('href', href);

	});

	$('.update_quantity').click(function(){

		var button = $(this);
		var url = '/manager/products.get_quantity/' + button.attr('data-pid');

		//call ajax
		button.siblings('.quantity_text').load(url);
	});

});//ready
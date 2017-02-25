$(function(){

	$('.delete-btn').click(function(event){
		//cancel default behavior
		event.preventDefault();

		//Modal
		$('#deleteUserModal').modal({
			//no options
		});

		var href = $(this).attr('href');
		$('#delete-confirm').attr('href', href);

	});

});//ready
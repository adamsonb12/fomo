$(function(){

	$('.img-responsive').click(function(event){

		//Modal
		$('#images_modal').modal({
			//no options
		});
	});

	var images = $('#modal-images img');
	var currentImageNum = 0;

	function showPic() {
		
		images.hide(800);
		var current = $(images[currentImageNum]);
		current.show(800);
	}
	//show first image
	showPic(currentImageNum);

	//buttons 
	$('#next').click(function() {
		currentImageNum++;
		if (currentImageNum == images.length)
		{
			currentImageNum = 0;
		}
		showPic();
	});//click

	//buttons 
	$('#previous').click(function() {
		currentImageNum--;
		if (currentImageNum < 0)
		{
			currentImageNum = images.length - 1;
		}
		showPic();
	});//click

});//ready
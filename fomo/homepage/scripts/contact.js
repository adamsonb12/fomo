// Jquery is pretty simple, 
// 
// gets the dom elements off of the dom
//
// Keep JS names and variables inside function curly braces -> Never in the Global scope


/*function doSomething() {

	console.log('ransomething');

}

$(doSomething);*/

// OR

/*$(function () {

	console.log('ransomething');

});*/

$(function() {
	var contactType = $(id_contactType);

	contactType.change(function() {
		var value = contactType.val();
		if(value == 'phone') {
			$('#id_phone').closest('p').show();
			$('#id_cellnumber').closest('p').show();
			$('#id_email').closest('p').hide();
		}
		else
		{
			$('#id_phone').closest('p').hide();
			$('#id_cellnumber').closest('p').hide();
			$('#id_email').closest('p').show();
		}
	})

});
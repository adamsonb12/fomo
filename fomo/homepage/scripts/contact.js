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
	var contacttype = $(id_contacttype);

	contacttype.change(function() {
		var value = contacttype.val();
		if(value == 'phone') {
			$('.contacttype-phone').closest('p').show(1000);
			$('.contacttype-email').closest('p').hide(1000);
		}
		else
		{
			$('.contacttype-phone').closest('p').hide(1000);
			$('.contacttype-email').closest('p').show(1000);
		}
	});
	contacttype.change();

});
def Last5ProductsMiddleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        print('2222222222222222222 Begin Middle Ware')
        # the view (and later middleware) are called.
        request.last5 = request.session.get('last5')
        if request.last5 is None:
        	request.last5 = []
        request.last5 = request.last5

 
        # let Django continue the processing and calls view function
        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        print('2222222222222222222 end Middle Ware')
        request.session['last5'] = request.last5[:5 ]
        return response

    return middleware
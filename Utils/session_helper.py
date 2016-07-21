def get_toast_and_cleanup_session(request):
    toast = None
    if request.session.get('toast'):
        toast = request.session.get('toast')
        del request.session['toast']
    return toast
from Settings.models import Setting


def website_name(request):
    site_name = "InvoiceGen"

    site_name_objects = Setting.objects.filter(key='site_name')
    if site_name_objects.count() != 0:
        site_name = site_name_objects[0].value

    return {'site_name': site_name}


def color_up(request):
    color_up = "#009688"

    color_up_objects = Setting.objects.filter(key='color_up')
    if color_up_objects.count() != 0:
        color_up = color_up_objects[0].value

    return {'color_up': color_up}


def color_down(request):
    color_down = "#009688"

    color_down_objects = Setting.objects.filter(key='color_down')
    if color_down_objects.count() != 0:
        color_down = color_down_objects[0].value

    return {'color_down': color_down}

def attach_toast_to_response(request):
    toast = None
    if request.session.get('toast'):
        toast = request.session.get('toast')
        del request.session['toast']

    return {'toast': toast}

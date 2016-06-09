def website_name(request):
    from Settings.models import Setting
    site_name_objects = Setting.objects.filter(key='site_name')
    if site_name_objects.count() != 0:
        site_name = site_name_objects[0].value
    else:
        site_name = "InvoiceGen"
    return {'site_name': site_name}


def color_up(request):
    from Settings.models import Setting
    color_up_objects = Setting.objects.filter(key='color_up')
    if color_up_objects.count() != 0:
        color_up = color_up_objects[0].value
    else:
        color_up = "#607d8b"
    return {'color_up': color_up}


def color_down(request):
    from Settings.models import Setting
    color_down_objects = Setting.objects.filter(key='color_down')
    if color_down_objects.count() != 0:
        color_down = color_down_objects[0].value
    else:
        color_down = "#e65100"
    return {'color_down': color_down}
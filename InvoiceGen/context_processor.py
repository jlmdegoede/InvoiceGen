def website_name(request):
    from Settings.models import Setting
    site_name_objects = Setting.objects.filter(key='site_name')
    if site_name_objects.count() != 0:
        site_name = site_name_objects[0].site_name
    else:
        site_name = "InvoiceGen"
    return {'site_name': site_name}
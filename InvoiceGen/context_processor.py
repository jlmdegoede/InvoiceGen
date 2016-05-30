def website_name(request):
    from FactuurMaker.models import UserSetting
    site_name_objects = UserSetting.objects.all()
    if site_name_objects.count() != 0:
        site_name = site_name_objects[0].site_name
    else:
        site_name = "FactuurMaker"
    return {'site_name': site_name}
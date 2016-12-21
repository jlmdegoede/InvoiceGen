from django.contrib.auth.models import Group, ContentType, Permission


def add_user_to_groups(new_user, groups):
    for group in groups:
        new_user.groups.add(group)
    new_user.save()


def create_agreement_group():
    group = Group.objects.get_or_create(name='Overeenkomsten')
    group = group[0]
    content_type = ContentType.objects.get(model='agreementtext')
    all_permissions = list(Permission.objects.filter(content_type=content_type))
    content_type = ContentType.objects.get(model='agreement')
    all_permissions += list(Permission.objects.filter(content_type=content_type))
    group.permissions.set(all_permissions)
    group.save()


def create_company_group():
    group = Group.objects.get_or_create(name='Opdrachtgevers')
    group = group[0]
    content_type = ContentType.objects.get(model='company')
    all_permissions = Permission.objects.filter(content_type=content_type)
    group.permissions.set(all_permissions)
    group.save()


def create_invoice_group():
    group = Group.objects.get_or_create(name='Facturen')
    group = group[0]
    content_type = ContentType.objects.get(model='outgoinginvoice')
    all_permissions = list(Permission.objects.filter(content_type=content_type))
    content_type = ContentType.objects.get(model='incominginvoice')
    all_permissions += list(Permission.objects.filter(content_type=content_type))
    all_permissions += [Permission.objects.filter(codename='view_invoice')[0]]
    group.permissions.set(all_permissions)
    group.save()


def create_order_group():
    group = Group.objects.get_or_create(name='Opdrachten')
    group = group[0]
    content_type = ContentType.objects.get(model='product')
    all_permissions = Permission.objects.filter(content_type=content_type)
    group.permissions.set(all_permissions)
    group.save()


def create_settings_group():
    group = Group.objects.get_or_create(name='Instellingen')
    group = group[0]
    content_type = ContentType.objects.get(model='setting')
    all_permissions = Permission.objects.filter(content_type=content_type)
    group.permissions.set(all_permissions)
    group.save()


def create_statistics_group():
    group = Group.objects.get_or_create(name='Statistieken')
    group = group[0]
    content_type = ContentType.objects.get(app_label='statistics')
    all_permissions = Permission.objects.filter(content_type=content_type)
    group.permissions.set(all_permissions)
    group.save()


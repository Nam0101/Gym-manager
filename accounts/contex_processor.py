

def contex_processor(request):
    from django.contrib.auth.models import Group
    member_group = Group.objects.get(name='MEMBER')
    manager_group = Group.objects.get(name='MANAGER')
    admin_group = Group.objects.get(name='admin')
    if member_group in request.user.groups.all():
        context = {'permission_level': 'reviews'}
    elif manager_group in request.user.groups.all():
        context = {'permission_level': 'manager'}
    elif admin_group in request.user.groups.all():
        context = {'permission_level': 'all'}
    else:
        context = {'permission_level': 'none'}
    # print(context)
    return context

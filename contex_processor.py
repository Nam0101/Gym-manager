from django.contrib.auth.models import Group


def contex_processor(request):
    # there is 3 group in our system : ADMIN, MEMBER, MANAGER
    # check if user is in MEMBER group
    member_group = Group.objects.get(name='MEMBER')
    # check if user is in MANAGER group
    manager_group = Group.objects.get(name='MANAGER')
    # check if user is in ADMIN group
    admin_group = Group.objects.get(name='admin')
    if member_group in request.user.groups.all():
        # User is in MEMBER group
        context = {'permission_level': 'reviews'}
    elif manager_group in request.user.groups.all():
        # User is in MANAGER group
        context = {'permission_level': 'manager'}
    elif admin_group in request.user.groups.all():
        # User is in ADMIN group
        context = {'permission_level': 'all'}
    else:
        # User is not in any group
        context = {'permission_level': 'none'}
    return context

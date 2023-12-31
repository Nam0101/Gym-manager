from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import csv
import datetime

import dateutil.parser as parser
import dateutil.relativedelta as delta
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.signals import post_save
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from equipment.models import Room
from notifications.config import get_notification_count
from notifications.config import my_handler
from payments.models import Payments
from trainers.models import Trainer
from .models import Member, Manager, Training_history, Subscription
from .forms import AddMemberForm, SearchForm, AddManagerForm, UpdateMemberGymForm, UpdateMemberInfoForm


def model_save(model):
    post_save.disconnect(my_handler, sender=Member)
    model.save()
    post_save.connect(my_handler, sender=Member)


def check_status(request, object):
    object.stop = 1 if request.POST.get('stop') == '1' else 0
    return object


# Export user information.
def export_all(user_obj):
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(['First name', 'Last name', 'Mobile', 'Admission Date', 'Subscription Type', 'Batch'])
    members = user_obj.values_list('first_name', 'last_name', 'mobile_number', 'admitted_on', 'subscription_type',
                                   'batch')
    for user in members:
        first_name = user[0]
        last_name = user[1]
        writer.writerow(user)

    response['Content-Disposition'] = 'attachment; filename="' + first_name + ' ' + last_name + '.csv"'
    return response


def members(request):
    form = AddMemberForm()
    context = {
        'form': form,
        'subs_end_today_count': get_notification_count(),
    }
    return render(request, 'add_member.html', context)


def view_manager(request):
    current_user = request.user
    if current_user.is_superuser:
        view_all = Manager.objects.all()
    else:
        view_all = Manager.objects.filter(user=current_user)
    paginator = Paginator(view_all, 100)
    try:
        page = request.GET.get('page', 1)
        view_all = paginator.page(page)
    except PageNotAnInteger:
        view_all = paginator.page(1)
    except EmptyPage:
        view_all = paginator.page(paginator.num_pages)
    search_form = SearchForm()
    context = {
        'all': view_all,
        'search_form': search_form,
        'subs_end_today_count': get_notification_count(),
    }
    return render(request, 'view_manager.html', context)


@login_required
def view_member(request):
    current_user = request.user
    if current_user.is_superuser:
        view_all = Member.objects.all()
        evening = Member.objects.filter(Q(batch='evening') | Q(batch='both'), stop=0).order_by('first_name')
        morning = Member.objects.filter(Q(batch='morning') | Q(batch='both'), stop=0).order_by('first_name')
        stopped = Member.objects.filter(stop=1).order_by('first_name')
    else:
        current_manager = Manager.objects.select_related('room').get(user=current_user)
        current_room = current_manager.room
        view_all = Member.objects.filter(room=current_room)
        evening = Member.objects.filter(Q(batch='evening') | Q(batch='both'), stop=0, room=current_room).order_by('first_name')
        morning = Member.objects.filter(Q(batch='morning') | Q(batch='both'), stop=0, room=current_room).order_by('first_name')
        stopped = Member.objects.filter(stop=1, room=current_room).order_by('first_name')
    paginator = Paginator(view_all, 100)
    page = request.GET.get('page', 1)
    try:
        view_all = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        view_all = paginator.get_page(1)
    search_form = SearchForm()
    context = {
        'all': view_all,
        'morning': morning,
        'evening': evening,
        'stopped': stopped,
        'search_form': search_form,
        'subs_end_today_count': get_notification_count(),
    }
    return render(request, 'view_member.html', context)


def create_user(request, member):
    username = member.first_name.lower() + member.last_name.lower()
    password = member.mobile_number
    user = User.objects.create_user(username=username, password=password)
    member.user = user
    member.save()

# def save_member(request, member):
#     member.first_name = request.POST.get('first_name').capitalize()
#     member.last_name = request.POST.get('last_name').capitalize()
#     member.registration_upto = parser.parse(request.POST.get('registration_date')) + delta.relativedelta(
#         months=int(request.POST.get('subscription_period')))
#     member.subscription_type = request.POST.get('subscription_type')
#     member.batch = request.POST.get('batch')
#     member.fee_status = request.POST.get('fee_status')
#     member.mobile_number = request.POST.get('mobile_number')
#     member.email = request.POST.get('email')
#     member.address = request.POST.get('address')
#     member.admitted_on = parser.parse(request.POST.get('admitted_on'))
#     member.fee = request.POST.get('fee')
#     member.save()
#

def add_member(request):
    view_all = Member.objects.all()
    success = None
    member = None
    if request.method == 'POST':
        form = AddMemberForm(request.POST, request.FILES)
        if form.is_valid():
            temp = form.save(commit=False)
            temp.first_name = request.POST.get('first_name').capitalize()
            temp.last_name = request.POST.get('last_name').capitalize()
            temp.registration_upto = parser.parse(request.POST.get('registration_date')) + delta.relativedelta(
                months=int(request.POST.get('subscription_period')))
            if request.POST.get('fee_status') == 'pending':
                temp.notification = 1
            password = temp.mobile_number
            username = temp.mobile_number
            user = User.objects.create_user(username=username, password=password)
            current_user = request.user
            current_room = Manager.objects.get(user=current_user).room
            temp.room = current_room
            month_paid = int(temp.subscription_period)
            if month_paid % 12 == 0:
                price = Subscription.objects.get(subscription_type=temp.subscription_type).price_per_year
                month_paid = month_paid / 12
            else:
                price = Subscription.objects.get(subscription_type=temp.subscription_type).price_per_month
            temp.amount = month_paid * price
            temp.user = user
            group = Group.objects.get(name='MEMBER')
            user.groups.add(group)
            member = temp
            member.save()
            success = 'Successfully Added Member'

            if temp.fee_status == 'paid':
                payments = Payments(
                    user=temp,
                    payment_date=temp.registration_date,
                    payment_period=temp.subscription_period,
                    payment_amount=temp.amount
                )
                payments.save()
            form = AddMemberForm()
            member = Member.objects.last()
        else:
            print(form.errors)
    else:
        form = AddMemberForm()

    context = {
        'add_success': success,
        'form': form,
        'member': member,
        'subs_end_today_count': get_notification_count(),
    }
    return render(request, 'add_member.html', context)


def view_member_detail(request):
    member = Member.objects.get(user=request.user)
    context = {
        'member': member,
    }
    return render(request, 'view_member_detail.html', context)


def view_training_history(request):
    current_user = request.user
    try:
        member = Member.objects.get(user=current_user)
        training_history = Training_history.objects.filter(member=member)
        context = {
            'member': member,
            'training_history': training_history,
        }
        return render(request, 'view_training_history_member.html', context)
    except Member.DoesNotExist:
        trainer = Trainer.objects.get(user=current_user)
        training_history = Training_history.objects.filter(trainer=trainer)
        context = {
            'trainer': trainer,
            'training_history': training_history,
        }
        return render(request, 'view_training_history.html', context)


def search_member(request):
    if request.method == 'POST':
        if 'clear' in request.POST:
            return redirect('view_member')
        search_form = SearchForm(request.POST)
        result = 0
        if search_form.is_valid():
            first_name = request.POST.get('search')
            result = Member.objects.filter(first_name__contains=first_name)

        view_all = Member.objects.all()
        evening = Member.objects.filter(batch='evening')
        morning = Member.objects.filter(batch='morning')
        both = Member.objects.filter(batch='both')
        # member in both is in both morning and evening batch
        evening = evening.exclude(pk__in=both)
        morning = morning.exclude(pk__in=both)
        context = {
            'all': view_all,
            'morning': morning,
            'evening': evening,
            'search_form': search_form,
            'result': result,
            'subs_end_today_count': get_notification_count(),
        }
        return render(request, 'view_member.html', context)
    else:
        search_form = SearchForm()
    return render(request, 'view_member.html', {'search_form': search_form})


def delete_member(request, id):
    Member.objects.filter(pk=id).delete()
    return redirect('view_member')


def update_member(request, id):
    if request.method == 'POST' and request.POST.get('export'):
        return export_all(Member.objects.filter(pk=id))
    if request.method == 'POST' and request.POST.get('no'):
        return redirect('/')
    if request.method == 'POST' and request.POST.get('gym_membership'):
        gym_form = UpdateMemberGymForm(request.POST)
        if gym_form.is_valid():
            object = Member.objects.get(pk=id)
            amount = request.POST.get('amount')
            day = (parser.parse(request.POST.get('registration_upto')) - delta.relativedelta(
                months=int(request.POST.get('subscription_period')))).day
            last_day = parser.parse(str(object.registration_upto)).day

            month = parser.parse(request.POST.get('registration_upto')).month
            last_month = parser.parse(str(object.registration_upto)).month
            # if status is stopped then do not update anything
            if object.stop == 1 and not request.POST.get('stop') == '0' and request.POST.get('gym_membership'):
                messages.error(request, 'Please start the status of user to update the record')
                return redirect('update_member', id=object.pk)
            # to change only the batch
            elif object.batch != request.POST.get('batch'):
                object.batch = request.POST.get('batch')
                object = check_status(request, object)
                model_save(object)
            # check if user has modified only the date
            elif (datetime.datetime.strptime(str(object.registration_date), "%Y-%m-%d") != datetime.datetime.strptime(
                    request.POST.get('registration_date'), "%Y-%m-%d")):
                object.registration_date = parser.parse(request.POST.get('registration_date'))
                object.registration_upto = parser.parse(request.POST.get('registration_date')) + delta.relativedelta(
                    months=int(request.POST.get('subscription_period')))
                object.fee_status = request.POST.get('fee_status')
                object = check_status(request, object)
                model_save(object)
            # if amount and period are changed
            elif (object.amount != amount) and (object.subscription_period != request.POST.get('subscription_period')):
                object.subscription_type = request.POST.get('subscription_type')
                object.subscription_period = request.POST.get('subscription_period')
                object.registration_date = parser.parse(request.POST.get('registration_upto'))
                object.registration_upto = parser.parse(request.POST.get('registration_upto')) + delta.relativedelta(
                    months=int(request.POST.get('subscription_period')))
                object.fee_status = request.POST.get('fee_status')
                object.amount = request.POST.get('amount')
                object = check_status(request, object)
                model_save(object)
            # if only subscription_period is Changed
            elif object.subscription_period != request.POST.get('subscription_period'):
                object.subscription_period = request.POST.get('subscription_period')
                object = check_status(request, object)
                model_save(object)
            # if amount and type are changed
            elif (object.amount != amount) and (object.subscription_type != request.POST.get('subscription_type')):
                object.subscription_type = request.POST.get('subscription_type')
                object.subscription_period = request.POST.get('subscription_period')
                object.registration_date = parser.parse(request.POST.get('registration_upto'))
                object.registration_upto = parser.parse(request.POST.get('registration_upto')) + delta.relativedelta(
                    months=int(request.POST.get('subscription_period')))
                object.fee_status = request.POST.get('fee_status')
                object.amount = request.POST.get('amount')
                object = check_status(request, object)
                model_save(object)
            # if amount ad fee status are changed
            elif (object.amount != amount) and (
                    (request.POST.get('fee_status') == 'paid') or (request.POST.get('fee_status') == 'pending')):
                object.amount = amount
                object.fee_status = request.POST.get('fee_status')
                object = check_status(request, object)
                model_save(object)
            # if only amount is channged
            elif object.amount != amount:
                object.registration_date = parser.parse(request.POST.get('registration_upto'))
                object.registration_upto = parser.parse(request.POST.get('registration_upto')) + delta.relativedelta(
                    months=int(request.POST.get('subscription_period')))
                object.fee_status = request.POST.get('fee_status')
                object.amount = request.POST.get('amount')
                if request.POST.get('fee_status') == 'pending':
                    object.notification = 1
                elif request.POST.get('fee_status') == 'paid':
                    object.notification = 2
                object = check_status(request, object)
                model_save(object)
            # nothing is changed
            else:
                if not request.POST.get('stop') == '1':
                    object.registration_date = parser.parse(request.POST.get('registration_upto'))
                    object.registration_upto = parser.parse(
                        request.POST.get('registration_upto')) + delta.relativedelta(
                        months=int(request.POST.get('subscription_period')))
                    object.amount = request.POST.get('amount')
                    if request.POST.get('fee_status') == 'pending':
                        object.notification = 1
                    elif request.POST.get('fee_status') == 'paid':
                        object.notification = 2
                object.fee_status = request.POST.get('fee_status')
                object = check_status(request, object)
                model_save(object)

            # Add payments if payment is 'paid'
            if object.fee_status == 'paid':
                check = Payments.objects.filter(
                    payment_date=object.registration_date,
                    user__pk=object.pk).count()
                if check == 0:
                    payments = Payments(
                        user=object,
                        payment_date=object.registration_date,
                        payment_period=object.subscription_period,
                        payment_amount=object.amount)
                    payments.save()
            user = Member.objects.get(pk=id)
            gym_form = UpdateMemberGymForm(initial={
                'registration_date': user.registration_date,
                'registration_upto': user.registration_upto,
                'subscription_type': user.subscription_type,
                'subscription_period': user.subscription_period,
                'amount': user.amount,
                'fee_status': user.fee_status,
                'batch': user.batch,
                'stop': user.stop,
            })

            info_form = UpdateMemberInfoForm(initial={
                'first_name': user.first_name,
                'last_name': user.last_name,
                'dob': user.dob,
            })

            try:
                payments = Payments.objects.filter(user=user)
            except Payments.DoesNotExist:
                payments = 'No Records'
            messages.success(request, 'Record updated successfully!')
            return redirect('update_member', id=user.pk)
        else:
            user = Member.objects.get(pk=id)
            info_form = UpdateMemberInfoForm(initial={
                'first_name': user.first_name,
                'last_name': user.last_name,
                'dob': user.dob,
            })

            try:
                payments = Payments.objects.filter(user=user)
            except Payments.DoesNotExist:
                payments = 'No Records'
            return render(request,
                          'update.html',
                          {
                              'payments': payments,
                              'gym_form': gym_form,
                              'info_form': info_form,
                              'user': user,
                              'subs_end_today_count': get_notification_count(),
                          })
    elif request.method == 'POST' and request.POST.get('info'):
        object = Member.objects.get(pk=id)
        object.first_name = request.POST.get('first_name')
        object.last_name = request.POST.get('last_name')
        object.dob = request.POST.get('dob')

        # for updating photo
        if 'photo' in request.FILES:
            myfile = request.FILES['photo']
            fs = FileSystemStorage(base_url="")
            photo = fs.save(myfile.name, myfile)
            object.photo = fs.url(photo)
        model_save(object)

        user = Member.objects.get(pk=id)
        gym_form = UpdateMemberGymForm(initial={
            'registration_date': user.registration_date,
            'registration_upto': user.registration_upto,
            'subscription_type': user.subscription_type,
            'subscription_period': user.subscription_period,
            'amount': user.amount,
            'fee_status': user.fee_status,
            'batch': user.batch,
            'stop': user.stop,
        })

        info_form = UpdateMemberInfoForm(initial={
            'first_name': user.first_name,
            'last_name': user.last_name,
            'dob': user.dob,
        })

        try:
            payments = Payments.objects.filter(user=user)
        except Payments.DoesNotExist:
            payments = 'No Records'

        return render(request,
                      'update.html',
                      {
                          'payments': payments,
                          'gym_form': gym_form,
                          'info_form': info_form,
                          'user': user,
                          'updated': 'Record Updated Successfully',
                          'subs_end_today_count': get_notification_count(),
                      })
    else:
        user = Member.objects.get(pk=id)

        if len(Payments.objects.filter(user=user)) > 0:
            payments = Payments.objects.filter(user=user)
        else:
            payments = 'No Records'
        gym_form = UpdateMemberGymForm(initial={
            'registration_date': user.registration_date,
            'registration_upto': user.registration_upto,
            'subscription_type': user.subscription_type,
            'subscription_period': user.subscription_period,
            'amount': user.amount,
            'fee_status': user.fee_status,
            'batch': user.batch,
            'stop': user.stop,
        })

        info_form = UpdateMemberInfoForm(initial={
            'first_name': user.first_name,
            'last_name': user.last_name,
            'dob': user.dob,
        })
        return render(request,
                      'update.html',
                      {
                          'payments': payments,
                          'gym_form': gym_form,
                          'info_form': info_form,
                          'user': user,
                          'subs_end_today_count': get_notification_count(),
                      }
                      )


def add_manager(request):
    success = None
    rooms = Room.objects.all()

    if request.method == 'POST':
        form = AddManagerForm(request.POST, request.FILES)
        if form.is_valid():
            manager = form.save(commit=False)
            manager.manager_name = request.POST.get('manager_name').capitalize()
            manager.manager_email = request.POST.get('manager_email')
            manager.manager_phone = request.POST.get('manager_phone')
            manager.manager_address = request.POST.get('manager_address')
            manager.dob = parser.parse(request.POST.get('dob'))
            manager.photo = request.FILES.get('photo')

            room_id = request.POST.get('room')
            room = Room.objects.get(pk=room_id)
            manager.room = room

            manager.save()

            # Create a user account for the manager
            username = manager.manager_email
            password = manager.manager_phone
            user = User.objects.create_user(username=username, password=password)
            manager.user = user
            manager.save()

            group = Group.objects.get(name='MANAGER')
            user.groups.add(group)

            success = 'Successfully Added Manager'

            form = AddManagerForm()
        else:
            print(form.errors)
    else:
        form = AddManagerForm()

    context = {
        'add_success': success,
        'form': form,
        'rooms': rooms,
        'subs_end_today_count': get_notification_count(),
    }
    return render(request, 'add_manager.html', context)
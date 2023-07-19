from django.shortcuts import render, redirect
from django.http import HttpResponse
from members.models import Member
import csv
import datetime

from payments.models import Payments
from .models import GenerateReportForm
from django.db.models import Q
from notifications.config import get_notification_count

REPORT_CHOICES = (
    ('member', 'Member'),
    ('equipment', 'Equipment'),
)


# Create your views here.
def export_all(user_obj):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'
    writer = csv.writer(response)
    writer.writerow(['First name', 'Last name', 'DOB', 'Mobile', 'Admission Date', 'Subscription Type', 'Batch'])
    members = user_obj.values_list('first_name', 'last_name', 'dob', 'mobile_number', 'admitted_on',
                                   'subscription_type', 'batch')
    for user in members:
        writer.writerow(user)

    return response


# def report_revenue(request):
#     context = {}
#     if request.method == 'POST':
#         form = GenerateReportForm(request.POST)
#         if form.is_valid():
#             if request.POST.get('month') and request.POST.get('year') and request.POST.get('batch'):
#                 query = Q(
#                     registration_date__month=request.POST.get('month'),
#                     registration_date__year=request.POST.get('year'),
#                     batch=request.POST.get('batch')
#                 )
#             elif request.POST.get('month') and request.POST.get('year'):
#                 query = Q(
#                     registration_date__month=request.POST.get('month'),
#                     registration_date__year=request.POST.get('year')
#                 )
#             elif request.POST.get('month') and request.POST.get('batch'):
#                 query = Q(
#                     registration_date__month=request.POST.get('month'),
#                     batch=request.POST.get('batch')
#                 )
#             elif request.POST.get('year') and request.POST.get('batch'):
#                 query = Q(
#                     registration_date__year=request.POST.get('year'),
#                     batch=request.POST.get('batch')
#                 )
#             elif request.POST.get('month'):
#                 query = Q(
#                     registration_date__month=request.POST.get('month')
#                 )
#             elif request.POST.get('year'):
#                 query = Q(
#                     registration_date__year=request.POST.get('year')
#                 )
#             elif request.POST.get('batch'):
#                 query = Q(
#                     batch=request.POST.get('batch')
#                 )
#             else:
#                 query = Q()
#             members = Member.objects.filter(query)
#             payment_amount = 0
#             for member in members:
#                 payment_amount += member.payment_amount
#             context['members'] = members
#             context['form'] = form
#             context['total_revenue'] = payment_amount
#             context['total_members'] = len(members)
#             return render(request, 'revenue.html', context)
#     else:
#         form = GenerateReportForm()
#         context['form'] = form
#         return render(request, 'revenue.html', context)

def convert_to_vnd_string(amount):
    amount = str(amount)
    amount = amount[::-1]
    amount = '.'.join([amount[i:i+3] for i in range(0, len(amount), 3)])
    amount = amount[::-1]
    amount = amount + ' VND'
    return amount

def reports(request):
    context = {}
    if request.method == 'POST':
        form = GenerateReportForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['report_type'] == 'member':
                if request.POST.get('month') and request.POST.get('year') and request.POST.get('batch'):
                    query = Q(
                        registration_date__month=request.POST.get('month'),
                        registration_date__year=request.POST.get('year'),
                        batch=request.POST.get('batch')
                    )
                elif request.POST.get('month') and request.POST.get('year'):
                    query = Q(
                        registration_date__month=request.POST.get('month'),
                        registration_date__year=request.POST.get('year')
                    )
                elif request.POST.get('month') and request.POST.get('batch'):
                    query = Q(
                        registration_date__month=request.POST.get('month'),
                        batch=request.POST.get('batch')
                    )
                elif request.POST.get('year') and request.POST.get('batch'):
                    query = Q(
                        registration_date__year=request.POST.get('year'),
                        batch=request.POST.get('batch')
                    )
                else:
                    query = Q(
                        registration_date__year=request.POST.get('year'),
                    )
                users = None
                if request.user.is_superuser:
                    users = Member.objects.filter(query)
                else:
                    users = Member.objects.filter(query, room=request.user.manager.room)
                if users is not None:
                    if 'export' in request.POST:
                        return export_all(users)
                    context = {
                        'users': users,
                        'form': form,
                        'subs_end_today_count': get_notification_count(),
                    }
                    return render(request, 'reports.html', context)
            elif form.cleaned_data['report_type'] == 'revenue':
                if request.POST.get('month') and request.POST.get('year') and request.POST.get('batch'):
                    query = Q(
                        registration_date__month=request.POST.get('month'),
                        registration_date__year=request.POST.get('year'),
                        batch=request.POST.get('batch')
                    )
                elif request.POST.get('month') and request.POST.get('year'):
                    query = Q(
                        registration_date__month=request.POST.get('month'),
                        registration_date__year=request.POST.get('year')
                    )
                elif request.POST.get('month') and request.POST.get('batch'):
                    query = Q(
                        registration_date__month=request.POST.get('month'),
                        batch=request.POST.get('batch')
                    )
                elif request.POST.get('year') and request.POST.get('batch'):
                    query = Q(
                        registration_date__year=request.POST.get('year'),
                        batch=request.POST.get('batch')
                    )
                elif request.POST.get('month'):
                    query = Q(
                        registration_date__month=request.POST.get('month')
                    )
                elif request.POST.get('year'):
                    query = Q(
                        registration_date__year=request.POST.get('year')
                    )
                elif request.POST.get('batch'):
                    query = Q(
                        batch=request.POST.get('batch')
                    )
                else:
                    query = Q()
                if request.user.is_superuser:
                    members = Member.objects.filter(query)
                else:
                    members = Member.objects.filter(query, room=request.user.manager.room)
                member_ids = []
                for member in members:
                    member_ids.append(member.member_id)
                payments = Payments.objects.filter(user_id__in=member_ids)
                payment_amount = 0
                for payment in payments:
                    payment_amount += payment.payment_amount
                context = {
                    'form': form,
                    'total_revenue': convert_to_vnd_string(payment_amount),
                    'total_members': len(members),
                    'subs_end_today_count': get_notification_count(),
                    'month': request.POST.get('month'),
                    'year': request.POST.get('year'),

                }
                return render(request, 'revenue.html', context)
    else:
        form = GenerateReportForm()
    return render(request, 'reports.html', {'form': form, 'subs_end_today_count': get_notification_count()})

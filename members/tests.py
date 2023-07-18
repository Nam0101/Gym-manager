from django.test import TestCase
from .models import Member
import datetime
from django.core.management import execute_from_command_line


# Create your tests here.
class MemberTestCase(TestCase):
    def setUp(self):
        Member.objects.create(
            first_name='test',
            last_name='test',
            mobile_number='80879966340',
            email='test@gmail.com',
            registration_date=datetime.datetime.now(),
            subscription_type='gym',
            subscription_period='1',
            amount='500',
            fee_status='paid',
            batch='morning',
        )

    def test_member(self):
        check = Member.objects.get(first_name='test')
        print(check)

from django.db import models


# Create your models here.
class business_revenue(models.Model):
    revenue_id = models.AutoField(primary_key=True)
    revenue_name = models.CharField(max_length=50)
    revenue_month = models.CharField(max_length=50)
    revenue_total = models.IntegerField()
    revenue_type = models.CharField(max_length=50)
    revenue_status = models.CharField(max_length=50)

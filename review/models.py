from django.db import models


# Create your models here.
class review(models.Model):
    review_id = models.AutoField(primary_key=True)
    member_name = models.CharField('Member Name', max_length=50)
    review_content = models.CharField('Review Content', max_length=300)
    review_date = models.DateField(auto_now_add=True)
    review_star = models.IntegerField('Review Star')

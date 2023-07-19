from django.db import models

from members.models import Member


# Create your models here.
class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, default=None,blank=True, null=True)
    review_content = models.CharField('Review Content', max_length=300)
    review_date = models.DateField(auto_now_add=True)
    review_star = models.IntegerField('Review Star')

    def __str__(self):
        return self.review_content



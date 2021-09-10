from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone_no = models.CharField(db_column='phone_no', null=True, max_length=100, default='')
    usage_flag = models.CharField(max_length=10, default='1')
    name = models.CharField(db_column='name', max_length=100)


    class Meta:
        db_table = "monitoring_profile"


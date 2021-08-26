from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone_no = models.CharField(db_column='phone_no', null=True, max_length=100, default='')
    usage_flag = models.CharField(max_length=10, default='1')

    class Meta:
        db_table = "monitoring_profile"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class mmProblem(models.Model):
    id = models.AutoField(primary_key=True)
    problem_name = models.CharField(db_column='problem_name', max_length=255, default='')
    model_func = models.CharField(db_column='model_func', max_length=255, default='')
    problem_note = models.CharField(db_column='problem_note', max_length=4096, default='')
    working_time = models.TimeField(db_column='working_time')
    created_at = models.DateTimeField(db_column='created_at', auto_now=True)
    delete_flag = models.CharField(db_column='delete_flag', max_length=10, default='0')

    class Meta:
        db_table = 'mm_problem'


class mmDataset(models.Model):
    id = models.AutoField(primary_key=True)
    problem_id= models.ForeignKey('mmproblem', on_delete=models.DO_NOTHING)
    data_static_path = models.CharField(db_column='data_static_path', max_length=255, default='')
    purpose = models.CharField(db_column='purpose', max_length=3, default='')
    data_name = models.CharField(db_column='data_name', max_length=255, default='')
    data_path = models.CharField(db_column='data_path', max_length=255, default='')
    data_cnt = models.IntegerField(db_column='data_cnt', default='0')
    data_size = models.IntegerField(db_column='data_size', default='0')
    created_at = models.DateTimeField(db_column='created_at', auto_now=True)
    delete_flag = models.CharField(db_column='delete_flag', max_length=10, default='0')

    class Meta:
        db_table = 'mm_dataset'


class mmModel(models.Model):
    id = models.AutoField(primary_key=True)
    dataset_id = models.ForeignKey('mmDataset', on_delete=models.DO_NOTHING)
    sensor_no = models.CharField(db_column='sensor_no', max_length=255, default='')
    threshold_std = models.FloatField(db_column='threshold_std', default='0')
    threshold_output = models.FloatField(db_column='threshold_output', default='0')
    threshold_adjust = models.FloatField(db_column='threshold_adjust', default='0')
    model_name = models.CharField(db_column='model_name', max_length=255, default='')
    model_name = models.CharField(db_column='model_name_en', max_length=255, default='')
    user_id = models.IntegerField(db_column='user_id')
    created_at = models.DateTimeField(db_column='created_at', auto_now=True)
    delete_flag = models.CharField(db_column='delete_flag', max_length=10, default='0')

    class Meta:
        db_table = 'mm_model'


class mmMonitoring(models.Model):
    id = models.AutoField(primary_key=True)
    model_id = models.ForeignKey('mmModel', on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(db_column='created_at', auto_now=True)
    warnlist_path = models.CharField(db_column='warnlist_path', max_length=255, default='')
    user_id = models.IntegerField(db_column='user_id')
    delete_flag = models.CharField(db_column='delete_flag', max_length=10, default='0')

    class Meta:
        db_table = 'mm_monitoring'
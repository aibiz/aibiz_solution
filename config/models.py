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
    equip_name = models.CharField(db_column='equip_name', max_length=50)
    chamber_name = models.CharField(db_column='chamber_name', max_length=50)
    recipe_name = models.CharField(db_column='recipe_name', max_length=50)
    revision_no = models.CharField(db_column='revision_no', max_length=50)
    data_static_path = models.CharField(db_column='data_static_path', max_length=255, default='')
    purpose = models.CharField(db_column='purpose', max_length=3, default='')
    data_name = models.CharField(db_column='data_name', max_length=255, default='')
    data_cnt = models.IntegerField(db_column='data_cnt', default='0')
    data_size = models.IntegerField(db_column='data_size', default='0')
    created_at = models.DateTimeField(db_column='created_at', auto_now=True)
    delete_flag = models.CharField(db_column='delete_flag', max_length=10, default='0')

    class Meta:
        db_table = 'mm_dataset'


class mmModel(models.Model):
    id = models.AutoField(primary_key=True)
    problem_id = models.IntegerField(db_column='problem_id')
    equipment_id = models.IntegerField(db_column='equipment_id')
    recipe_id = models.IntegerField(db_column='recipe_id')
    dataset = models.ForeignKey('mmDataset', on_delete=models.DO_NOTHING)
    sensor_cd = models.IntegerField(db_column='sensor_cd')
    model_name = models.CharField(db_column='model_name', max_length=255, default='')
    model_name_en = models.CharField(db_column='model_name_en', max_length=255, default='')
    user_id = models.IntegerField(db_column='user_id')
    created_at = models.DateTimeField(db_column='created_at', auto_now=True)
    delete_flag = models.CharField(db_column='delete_flag', max_length=10, default='0')

    class Meta:
        db_table = 'mm_model'


class mhMonitoring(models.Model):
    id = models.AutoField(primary_key=True)
    model = models.ForeignKey('mmModel', on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(db_column='created_at', auto_now=True)
    warnlist_path = models.CharField(db_column='warnlist_path', max_length=255, default='')
    user_id = models.IntegerField(db_column='user_id')
    delete_flag = models.CharField(db_column='delete_flag', max_length=10, default='0')

    class Meta:
        db_table = 'mh_monitoring'

class mmEquipspec(models.Model):
    id = models.AutoField(primary_key=True)
    equip_name = models.CharField(db_column='equip_name', max_length=50)
    chamber_cnt = models.IntegerField(db_column='chamber_cnt')
    sensor_cnt = models.IntegerField(db_column='sensor_cnt')

    class Meta:
        db_table = 'mm_equipspec'

class mmRecipe(models.Model):
    id = models.AutoField(primary_key=True)
    recipe_id = models.IntegerField(db_column='recipe_id')
    recipe_name = models.CharField(db_column='recipe_name', max_length=50)
    revision_no = models.CharField(db_column='revision_no', max_length=50)
    equip_name = models.CharField(db_column='equip_name', max_length=50)
    chamber_name = models.CharField(db_column='chamber_name', max_length=50)
    sensor_cd = models.IntegerField(db_column='sensor_cd')
    sensor_name = models.CharField(db_column='sensor_name', max_length=50)

    class Meta:
        db_table = 'mm_recipe'

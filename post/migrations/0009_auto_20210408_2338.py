# Generated by Django 3.1.7 on 2021-04-08 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0008_auto_20210408_2337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='model_year',
            field=models.CharField(blank=True, max_length=4, null=True, verbose_name='Car Model Year'),
        ),
        migrations.AlterField(
            model_name='post',
            name='reg_exp',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='variant',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Car Variant'),
        ),
        migrations.AlterField(
            model_name='post',
            name='vin',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Car VIN'),
        ),
    ]

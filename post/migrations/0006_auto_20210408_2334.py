# Generated by Django 3.1.7 on 2021-04-08 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0005_auto_20210408_2333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='start_time',
            field=models.DateField(auto_now_add=True),
        ),
    ]
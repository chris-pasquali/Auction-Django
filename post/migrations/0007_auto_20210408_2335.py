# Generated by Django 3.1.7 on 2021-04-08 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0006_auto_20210408_2334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='end_time',
            field=models.DateField(auto_now_add=True),
        ),
    ]

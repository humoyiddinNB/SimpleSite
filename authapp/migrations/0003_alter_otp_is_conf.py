# Generated by Django 5.2 on 2025-04-25 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0002_otp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otp',
            name='is_conf',
            field=models.BooleanField(default=False),
        ),
    ]

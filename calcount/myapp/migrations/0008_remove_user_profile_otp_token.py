# Generated by Django 5.0.2 on 2024-02-14 07:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_user_profile_otp_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_profile',
            name='otp_token',
        ),
    ]

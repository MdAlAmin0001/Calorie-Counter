# Generated by Django 5.0.1 on 2024-01-21 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_profile',
            name='gender',
            field=models.CharField(blank=True, choices=[('Male', 'male'), ('Female', 'female')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='user_profile',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]

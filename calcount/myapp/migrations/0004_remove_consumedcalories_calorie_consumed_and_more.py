# Generated by Django 5.0.1 on 2024-01-24 03:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_consumedcalories_dailyconsumedcaloriesform'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='consumedcalories',
            name='calorie_consumed',
        ),
        migrations.AddField(
            model_name='consumedcalories',
            name='calories_consumed',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='consumedcalories',
            name='date_consumed',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='consumedcalories',
            name='item_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.DeleteModel(
            name='DailyConsumedCaloriesForm',
        ),
    ]
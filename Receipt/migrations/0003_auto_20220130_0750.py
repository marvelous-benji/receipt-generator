# Generated by Django 3.1.12 on 2022-01-30 07:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("Receipt", "0002_auto_20220130_0747"),
    ]

    operations = [
        migrations.AlterField(
            model_name="receipthistory",
            name="date_issued",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
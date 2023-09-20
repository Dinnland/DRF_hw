# Generated by Django 4.2.4 on 2023-09-18 00:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_app', '0008_subscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='is_paid',
            field=models.BooleanField(default=False, verbose_name='статус оплаты'),
        ),
        migrations.AddField(
            model_name='payment',
            name='session',
            field=models.CharField(blank=True, max_length=180, null=True, verbose_name='сессия для оплаты'),
        ),
    ]
# Generated by Django 4.2.4 on 2023-09-18 01:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_app', '0009_payment_is_paid_payment_session'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_amount',
            field=models.IntegerField(verbose_name='сумма оплаты'),
        ),
    ]

# Generated by Django 2.2.5 on 2019-10-02 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_user_date_subscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='monthly_payment',
            field=models.IntegerField(default=350),
        ),
    ]

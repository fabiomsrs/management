# Generated by Django 2.2.5 on 2019-10-02 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_user_monthly_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='monthly_payment',
            field=models.IntegerField(default=350, verbose_name='Mensalidade'),
        ),
    ]

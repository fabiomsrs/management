# Generated by Django 2.2.5 on 2019-09-25 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_paymentregister_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentregister',
            name='payment_date',
            field=models.DateField(verbose_name='Data da efetuação do pagamento'),
        ),
    ]

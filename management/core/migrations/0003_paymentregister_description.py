# Generated by Django 2.2.5 on 2019-09-25 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20190925_0925'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentregister',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='descrição do pagamento'),
        ),
    ]

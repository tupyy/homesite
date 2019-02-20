# Generated by Django 2.1.7 on 2019-02-20 15:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('money', '0015_auto_20190220_0913'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='contract',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='nb_tickete',
        ),
        migrations.AlterField(
            model_name='payment',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='recurrentpayment',
            name='contract',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_NULL, to='contract.Contract'),
        ),
        migrations.AlterField(
            model_name='recurrentpayment',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]

# Generated by Django 2.0.1 on 2018-03-17 13:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('money', '0009_myevent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentoccurrence',
            name='payment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='money.MyEvent'),
        ),
    ]

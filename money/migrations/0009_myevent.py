# Generated by Django 2.0.1 on 2018-03-17 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('money', '0008_auto_20180317_1340'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=10)),
            ],
        ),
    ]
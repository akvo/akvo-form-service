# Generated by Django 4.2.1 on 2023-09-14 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_data', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='answers',
            name='repeat',
            field=models.IntegerField(default=0),
        ),
    ]
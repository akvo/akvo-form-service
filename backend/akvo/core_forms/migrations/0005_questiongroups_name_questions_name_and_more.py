# Generated by Django 4.2.1 on 2024-06-19 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            'core_forms',
            '0004_rename_name_options_label_rename_code_options_value_and_more'
        ),
    ]

    operations = [
        migrations.AddField(
            model_name='questiongroups',
            name='name',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='questions',
            name='name',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='questions',
            name='short_label',
            field=models.TextField(default=None, null=True),
        ),
    ]

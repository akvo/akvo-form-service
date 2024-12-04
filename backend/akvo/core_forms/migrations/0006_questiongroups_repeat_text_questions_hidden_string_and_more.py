# Generated by Django 4.2.1 on 2024-12-03 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_forms', '0005_questiongroups_name_questions_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='questiongroups',
            name='repeat_text',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='questions',
            name='hidden_string',
            field=models.BooleanField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='questions',
            name='limit',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='questions',
            name='required_double_entry',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='questiongroups',
            name='label',
            field=models.TextField(default=None, null=True),
        ),
    ]
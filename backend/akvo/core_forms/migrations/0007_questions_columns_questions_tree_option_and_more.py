# Generated by Django 4.2.1 on 2024-12-04 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_forms', '0006_questiongroups_repeat_text_questions_hidden_string_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='questions',
            name='columns',
            field=models.JSONField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='questions',
            name='tree_option',
            field=models.CharField(default=None, max_length=191, null=True),
        ),
        migrations.AlterField(
            model_name='questions',
            name='type',
            field=models.IntegerField(choices=[(2, 'input'), (3, 'text'), (4, 'number'), (1, 'geo'), (5, 'option'), (6, 'multiple_option'), (7, 'cascade'), (8, 'image'), (9, 'date'), (10, 'autofield'), (11, 'tree'), (12, 'table')]),
        ),
    ]

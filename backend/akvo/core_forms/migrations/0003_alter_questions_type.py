# Generated by Django 4.2.1 on 2023-09-21 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_forms', '0002_alter_questions_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questions',
            name='type',
            field=models.IntegerField(choices=[(2, 'input'), (3, 'text'), (4, 'number'), (1, 'geo'), (5, 'option'), (6, 'multiple_option'), (7, 'cascade'), (8, 'image'), (9, 'date'), (10, 'autofield')]),
        ),
    ]

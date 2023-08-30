# Generated by Django 4.2.1 on 2023-08-30 01:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core_forms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('geo', models.JSONField(default=None, null=True)),
                ('submitter', models.CharField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(default=None, null=True)),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='data', to='core_forms.forms')),
            ],
            options={
                'db_table': 'data',
            },
        ),
        migrations.CreateModel(
            name='Answers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(default=None, null=True)),
                ('value', models.FloatField(default=None, null=True)),
                ('options', models.JSONField(default=None, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(default=None, null=True)),
                ('data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='data_answers', to='core_data.data')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_answers', to='core_forms.questions')),
            ],
            options={
                'db_table': 'answers',
            },
        ),
    ]
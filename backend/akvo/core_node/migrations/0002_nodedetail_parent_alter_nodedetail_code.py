# Generated by Django 4.2.1 on 2023-09-04 21:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core_node', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='nodedetail',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='core_node.nodedetail'),
        ),
        migrations.AlterField(
            model_name='nodedetail',
            name='code',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
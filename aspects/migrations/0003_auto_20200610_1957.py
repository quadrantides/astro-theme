# Generated by Django 3.0.6 on 2020-06-10 19:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aspects', '0002_auto_20200610_1646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sunvenuscoverage',
            name='cycle',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='aspects.Cycle2', verbose_name='cycle'),
        ),
    ]

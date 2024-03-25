# Generated by Django 3.0.6 on 2020-06-20 07:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aspects', '0005_auto_20200618_1835'),
    ]

    operations = [
        migrations.AddField(
            model_name='cycle2',
            name='is_internal',
            field=models.BooleanField(default=False, verbose_name='is an internal cycle ?'),
        ),
        migrations.AlterField(
            model_name='cycle2',
            name='description',
            field=models.TextField(blank=True, verbose_name='Information complémentaire'),
        ),
        migrations.AlterField(
            model_name='cycle2',
            name='planet2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='aspects.Planet', verbose_name='planet 2'),
        ),
        migrations.AlterField(
            model_name='saturnjupiteraspect',
            name='active',
            field=models.BooleanField(default=False, verbose_name='Enregistrement actif ?'),
        ),
        migrations.AlterField(
            model_name='sunvenusaspect',
            name='active',
            field=models.BooleanField(default=False, verbose_name='Enregistrement actif ?'),
        ),
        migrations.AlterField(
            model_name='sunvenusconjunction',
            name='active',
            field=models.BooleanField(default=False, verbose_name='Enregistrement actif ?'),
        ),
        migrations.AlterField(
            model_name='sunvenusconjunction',
            name='true',
            field=models.BooleanField(default=False, verbose_name='Est-elle exacte ?'),
        ),
        migrations.AlterField(
            model_name='sunvenusconjunction',
            name='type',
            field=models.CharField(max_length=150, verbose_name='Type'),
        ),
    ]

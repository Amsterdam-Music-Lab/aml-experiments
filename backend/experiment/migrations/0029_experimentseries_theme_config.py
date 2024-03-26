# Generated by Django 3.2.25 on 2024-03-26 15:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('theme', '0005_footerconfig'),
        ('experiment', '0028_auto_20240325_1851'),
    ]

    operations = [
        migrations.AddField(
            model_name='experimentseries',
            name='theme_config',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='theme.themeconfig'),
        ),
    ]

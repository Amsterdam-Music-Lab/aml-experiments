# Generated by Django 4.2.17 on 2025-01-07 12:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('theme', '0007_sponsorimage_footerconfig_new_logos'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='footerconfig',
            name='disclaimer',
        ),
        migrations.RemoveField(
            model_name='footerconfig',
            name='privacy',
        ),
    ]

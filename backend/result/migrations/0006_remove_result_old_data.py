# Generated by Django 3.2.20 on 2023-11-26 09:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0005_rename_json_temp_to_json_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='result',
            name='old_data',
        ),
    ]

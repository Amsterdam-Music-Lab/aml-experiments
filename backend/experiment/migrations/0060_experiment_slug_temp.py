# Generated by Django 4.2.16 on 2024-11-15 09:00

from django.db import migrations, models
import experiment.validators


class Migration(migrations.Migration):

    dependencies = [
        ('experiment', '0059_add_social_media_config'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiment',
            name='slug_temp',
            field=models.SlugField(null=True, max_length=64, unique=True, validators=[experiment.validators.block_slug_validator]),
        ),
    ]

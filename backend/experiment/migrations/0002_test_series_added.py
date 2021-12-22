# Generated by Django 3.2.8 on 2021-12-16 12:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('experiment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestSeries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_experiments', models.JSONField(blank=True, default=dict, null=True)),
                ('random_experiments', models.JSONField(blank=True, default=dict, null=True)),
                ('last_experiments', models.JSONField(blank=True, default=dict, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='playlist',
            name='csv',
            field=models.TextField(blank=True, help_text='CSV Format: artist_name [string],        song_name [string], start_position [float], duration [float],        "path/filename.mp3" [string], restricted_to_nl [int 0=False 1=True], tag_id [int], group_id [int]'),
        ),
        migrations.AddField(
            model_name='experiment',
            name='test_series',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='experiment.testseries'),
        ),
    ]

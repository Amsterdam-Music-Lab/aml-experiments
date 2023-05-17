# Generated by Django 3.2.18 on 2023-05-15 13:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    def move_songs(apps, schema_editor):
        Section = apps.get_model('section', 'Section')
        Song = apps.get_model('section', 'Song')
        for section in Section.objects.all():
            if section.name and section.artist:
                song, created = Song.objects.get_or_create(artist=section.artist, name=section.name)
                if section.restrict_to_nl:
                    song.restricted = ['nl']
                section.song = song
                section.save()
    
    def move_songs_backwards(apps, schema_editor):
        Section = apps.get_model('section', 'Section')
        for section in Section.objects.all():
            section.name = ''
            section.artist = ''
            if section.song:
                section.name = section.song.name
                section.artist = section.song.artist
                if section.song.restricted.length:
                    section.restrict_to_nl = 1
            section.save()          


    dependencies = [
        ('section', '0002_alter_section_filename'),
    ]

    operations = [
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist', models.CharField(db_index=True, max_length=128)),
                ('name', models.CharField(db_index=True, max_length=128)),
                ('restricted', models.JSONField(default=list))
            ],
            options={
                'unique_together': {('artist', 'name')},
            },
        ),
        migrations.AddField(
            model_name='section',
            name='song',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='section.song'),
        ),
        migrations.AlterModelOptions(
            name='section',
            options={'ordering': ['song__artist', 'song__name', 'start_time']},
        ),
        migrations.RunPython(move_songs,  move_songs_backwards),
        migrations.RemoveField(
            model_name='section',
            name='artist',
        ),
        migrations.RemoveField(
            model_name='section',
            name='name',
        ),
        migrations.RemoveField(
            model_name='section',
            name='restrict_to_nl',
        ),
    ]

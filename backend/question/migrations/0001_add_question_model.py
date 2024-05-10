# Generated by Django 3.2.25 on 2024-05-09 11:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('experiment', '0034_add_question_model'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('key', models.CharField(max_length=128, primary_key=True, serialize=False)),
                ('question', models.CharField(max_length=1024)),
                ('editable', models.BooleanField(default=True, editable=False)),
            ],
            options={
                'ordering': ['key'],
            },
        ),
        migrations.CreateModel(
            name='QuestionInSeries',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.PositiveIntegerField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='question.question')),
            ],
            options={
                'verbose_name_plural': 'Question In Series objects',
                'ordering': ['index'],
            },
        ),
        migrations.CreateModel(
            name='QuestionSeries',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=128)),
                ('index', models.PositiveIntegerField()),
                ('randomize', models.BooleanField(default=False)),
                ('experiment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='experiment.experiment')),
                ('questions', models.ManyToManyField(through='question.QuestionInSeries', to='question.Question')),
            ],
            options={
                'verbose_name_plural': 'Question Series',
                'ordering': ['index'],
            },
        ),
        migrations.AddField(
            model_name='questioninseries',
            name='question_series',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='question.questionseries'),
        ),
        migrations.CreateModel(
            name='QuestionGroup',
            fields=[
                ('key', models.CharField(max_length=128, primary_key=True, serialize=False)),
                ('editable', models.BooleanField(default=True, editable=False)),
                ('questions', models.ManyToManyField(to='question.Question')),
            ],
            options={
                'verbose_name_plural': 'Question Groups',
                'ordering': ['key'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='questioninseries',
            unique_together={('question_series', 'question')},
        ),
    ]

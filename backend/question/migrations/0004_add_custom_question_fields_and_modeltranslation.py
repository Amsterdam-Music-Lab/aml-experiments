# Generated by Django 4.2.15 on 2024-10-13 12:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0003_rename_experiment_questionseries_block'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='explainer',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='question',
            name='explainer_en',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='explainer_nl',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='explainer_pt',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='is_skippable',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='question',
            name='max_length',
            field=models.IntegerField(default=64),
        ),
        migrations.AddField(
            model_name='question',
            name='max_value',
            field=models.FloatField(default=120),
        ),
        migrations.AddField(
            model_name='question',
            name='min_value',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='question',
            name='min_values',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='question',
            name='profile_scoring_rule',
            field=models.CharField(blank=True, choices=[('LIKERT', 'LIKERT'), ('REVERSE_LIKERT', 'REVERSE_LIKERT'), ('CATEGORIES_TO_LIKERT', 'CATEGORIES_TO_LIKERT')], default='', max_length=128),
        ),
        migrations.AddField(
            model_name='question',
            name='question_en',
            field=models.CharField(max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='question_nl',
            field=models.CharField(max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='question_pt',
            field=models.CharField(max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='scale_steps',
            field=models.IntegerField(choices=[(5, 5), (7, 7)], default=7),
        ),
        migrations.AddField(
            model_name='question',
            name='type',
            field=models.CharField(choices=[('', '---------'), ('BooleanQuestion', 'BooleanQuestion'), ('ChoiceQuestion', 'ChoiceQuestion'), ('NumberQuestion', 'NumberQuestion'), ('TextQuestion', 'TextQuestion'), ('LikertQuestion', 'LikertQuestion'), ('LikertQuestionIcon', 'LikertQuestionIcon'), ('AutoCompleteQuestion', 'AutoCompleteQuestion')], default='', max_length=128),
        ),
        migrations.AddField(
            model_name='question',
            name='view',
            field=models.CharField(choices=[('BUTTON_ARRAY', 'BUTTON_ARRAY'), ('CHECKBOXES', 'CHECKBOXES'), ('RADIOS', 'RADIOS'), ('DROPDOWN', 'DROPDOWN')], default='', max_length=128),
        ),
        migrations.AlterField(
            model_name='question',
            name='key',
            field=models.SlugField(max_length=128, primary_key=True, serialize=False),
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.SlugField(max_length=128)),
                ('text', models.CharField()),
                ('text_en', models.CharField(null=True)),
                ('text_nl', models.CharField(null=True)),
                ('text_pt', models.CharField(null=True)),
                ('index', models.PositiveIntegerField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='question.question')),
            ],
            options={
                'ordering': ['index'],
            },
        ),
    ]

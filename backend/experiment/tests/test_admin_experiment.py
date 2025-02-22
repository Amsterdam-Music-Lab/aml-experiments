from django.test import TestCase, RequestFactory
from django.contrib.admin.sites import AdminSite
from django.urls import reverse
from django.utils.html import format_html
from experiment.admin import ExperimentAdmin, PhaseAdmin
from experiment.models import Block, Experiment, Phase, ExperimentTranslatedContent, BlockTranslatedContent
from section.models import Playlist
from theme.models import ThemeConfig
from question.models import QuestionSeries, QuestionInSeries, Question
from question.questions import create_default_questions

# Expected field count per model
EXPECTED_BLOCK_FIELDS = 10
EXPECTED_SESSION_FIELDS = 8
EXPECTED_RESULT_FIELDS = 12
EXPECTED_PARTICIPANT_FIELDS = 5


class MockRequest:
    pass


request = MockRequest()

class TestExperimentAdmin(TestCase):
    @classmethod
    def setUpTestData(self):
        self.experiment = Experiment.objects.create(
            slug="TEST",
        )
        ExperimentTranslatedContent.objects.create(
            experiment=self.experiment,
            language="en",
            name="test",
            description="test description very long like the tea of oolong and the song of the bird in the morning",
        )

    def setUp(self):
        self.admin = ExperimentAdmin(model=Experiment, admin_site=AdminSite)

    def test_experiment_admin_list_display(self):
        self.assertEqual(
            ExperimentAdmin.list_display,
            (
                "name",
                "slug_link",
                "remarks",
                "active",
            ),
        )

    def test_experiment_admin_research_dashboard(self):
        request = RequestFactory().request()
        response = self.admin.experimenter_dashboard(request, self.experiment)
        self.assertEqual(response.status_code, 200)


class PhaseAdminTest(TestCase):
    def setUp(self):
        self.admin = PhaseAdmin(model=Phase, admin_site=AdminSite)

    def test_phase_admin_related_experiment_method(self):
        experiment = Experiment.objects.create(slug="test-experiment")
        ExperimentTranslatedContent.objects.create(experiment=experiment, language="en", name="Test Experiment")
        phase = Phase.objects.create(
            index=1, randomize=False, experiment=experiment, dashboard=True
        )
        related_experiment = self.admin.related_experiment(phase)
        expected_url = reverse("admin:experiment_experiment_change", args=[experiment.pk])
        expected_related_experiment = format_html(
            '<a href="{}">{}</a>', expected_url, experiment.get_fallback_content().name
        )
        self.assertEqual(related_experiment, expected_related_experiment)

    def test_experiment_with_no_blocks(self):
        experiment = Experiment.objects.create(slug="no-blocks")
        ExperimentTranslatedContent.objects.create(
            experiment=experiment,
            language="en",
            name="No Blocks",
        )
        phase = Phase.objects.create(
            index=1, randomize=False, dashboard=True, experiment=experiment
        )
        blocks = self.admin.blocks(phase)
        self.assertEqual(blocks, "No blocks")

    def test_experiment_with_blocks(self):
        experiment = Experiment.objects.create(slug="with-blocks")
        ExperimentTranslatedContent.objects.create(
            experiment=experiment,
            language="en",
            name="With Blocks",
        )
        phase = Phase.objects.create(
            index=1, randomize=False, dashboard=True, experiment=experiment
        )
        block1 = Block.objects.create(slug="block-1", phase=phase)
        block2 = Block.objects.create(slug="block-2", phase=phase)

        blocks = self.admin.blocks(phase)
        expected_blocks = format_html(
            ", ".join([f"{block.slug}" for block in [block1, block2]])
        )
        self.assertEqual(blocks, expected_blocks)


class TestDuplicateExperiment(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.experiment = Experiment.objects.create(slug="original")
        ExperimentTranslatedContent.objects.create(
            experiment=cls.experiment,
            language="en",
            name="original experiment",
        )
        ExperimentTranslatedContent.objects.create(
            experiment=cls.experiment,
            language="nl",
            name="origineel experiment",
        )
        cls.first_phase = Phase.objects.create(
            index=1, randomize=False, dashboard=True, experiment=cls.experiment
        )
        cls.second_phase = Phase.objects.create(
            index=2, randomize=False, dashboard=True, experiment=cls.experiment
        )
        cls.playlist1 = Playlist.objects.create(name="first")
        cls.playlist2 = Playlist.objects.create(name="second")
        cls.theme = ThemeConfig.objects.create(name='test_theme')

        cls.block1 = Block.objects.create(slug="block1", phase=cls.first_phase, theme_config=cls.theme)
        cls.block2 = Block.objects.create(slug="block2", phase=cls.first_phase, theme_config=cls.theme)
        cls.block3 = Block.objects.create(slug="block3", phase=cls.second_phase, theme_config=cls.theme)
        cls.block4 = Block.objects.create(slug="block4", phase=cls.second_phase, theme_config=cls.theme)

        cls.block1.playlists.add(cls.playlist1)
        cls.block1.playlists.add(cls.playlist2)
        cls.block1.save()
        create_default_questions()
        cls.question_series = QuestionSeries.objects.create(block=cls.block2, index=0)
        cls.questions = Question.objects.all()
        index = 0
        for question in cls.questions:
            QuestionInSeries.objects.create(question_series = cls.question_series,
                                            question=question,
                                            index=index)
            index += 1

        cls.questions_in_series = QuestionInSeries.objects.all()

        BlockTranslatedContent.objects.create(
            block=cls.block1,
            language="en",
            name="First block",
            description="Block1 description"
        )
        BlockTranslatedContent.objects.create(
            block=cls.block1,
            language="nl",
            name="Eerste blok",
            description="Block1 omschrijving"
        )
        BlockTranslatedContent.objects.create(
            block=cls.block2,
            language="en",
            name="Second block",
            description="Block2 description"
        )
        BlockTranslatedContent.objects.create(
            block=cls.block2,
            language="nl",
            name="Tweede blok",
            description="Block2 omschrijving"
        )
        BlockTranslatedContent.objects.create(
            block=cls.block3,
            language="en",
            name="Third block",
            description="Block3 description"
        )
        BlockTranslatedContent.objects.create(
            block=cls.block3,
            language="nl",
            name="Derde blok",
            description="Block3 omschrijving"
        )
        BlockTranslatedContent.objects.create(
            block=cls.block4,
            language="en",
            name="Fourth block",
            description="Block4 description"
        )
        BlockTranslatedContent.objects.create(
            block=cls.block4,
            language="nl",
            name="Vierde blok",
            description="Block4 omschrijving"
        )

    def setUp(self):
        self.admin = ExperimentAdmin(model=Experiment, admin_site=AdminSite)

    def test_duplicate_experiment(self):
        request = MockRequest()
        request.POST = {"_duplicate": "",
                        "slug-extension": "duplitest"}
        response = self.admin.duplicate(request, self.experiment)

        new_exp = Experiment.objects.last()
        all_experiments = Experiment.objects.all()
        all_exp_content = ExperimentTranslatedContent.objects.all()

        all_phases = Phase.objects.all()

        all_blocks = Block.objects.all()
        last_block = Block.objects.last()
        all_block_content = BlockTranslatedContent.objects.all()
        new_block1 = Block.objects.get(slug="block1-duplitest")

        all_question_series = QuestionSeries.objects.all()
        all_questions = Question.objects.all()

        self.assertEqual(all_experiments.count(), 2)
        self.assertEqual(all_exp_content.count(), 4)
        self.assertEqual(new_exp.slug, 'original-duplitest')

        self.assertEqual(all_phases.count(), 4)

        self.assertEqual(all_blocks.count(), 8)
        self.assertEqual(all_block_content.count(), 16)
        self.assertEqual(last_block.slug, 'block4-duplitest')
        self.assertEqual(last_block.theme_config.name, 'test_theme')

        self.assertEqual(new_block1.playlists.all().count(), 2)

        self.assertEqual(all_question_series.count(), 2)
        self.assertEqual(self.questions.count(), (all_questions.count()))

        self.assertEqual(response.status_code, 302)

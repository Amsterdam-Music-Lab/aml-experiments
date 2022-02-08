from django.utils.translation import gettext_lazy as _

from experiment.models import Section
from .views import Trial, Explainer
from .views.form import ChoiceQuestion, Form
from .views.playback import Playback

from .base import Base
from .h_bat import HBat

from .util.actions import final_action_with_optional_button
from .util.score import get_average_difference_level_based

class BST(HBat):
    """ Rules for the BST experiment, which follow closely
    the HBAT rules. """
    ID = 'BST'

    @classmethod
    def intro_explainer(cls):
        return Explainer.action(
            instruction=_(
                'In this test you will hear a number of rhythms which have a regular beat.'),
            steps=[
                Explainer.step(
                    description=_(
                        "It's your job to decide if the rhythm has a DUPLE METER (a MARCH) or a TRIPLE METER (a WALTZ)."),
                    number=1
                ),
                Explainer.step(
                    description=_("Every SECOND tone in a DUPLE meter (march) is louder and every THIRD tone in a TRIPLE meter (waltz) is louder."),
                    number=2
                ),
                Explainer.step(
                    description=_(
                        'During the experiment it will become more difficult to hear the difference.'),
                    number=3
                ),
                Explainer.step(
                    description=_(
                        "Try to answer as accurately as possible, even if you're uncertain."),
                    number=4
                ),
                Explainer.step(
                    description=_(
                        "In this test, you can answer as soon as you feel you know the answer."),
                    number=5
                ),
                Explainer.step(
                    description=_(
                        "NOTE: Please wait with answering until you are either sure, or the sound has stopped."),
                    number=6
                ),
                Explainer.step(
                    description=_(
                        'This test will take around 4 minutes to complete. Try to stay focused for the entire test!'),
                    number=7
                )],
            button_label='Ok'
        )

    @classmethod
    def next_trial_action(cls, session, trial_condition, level=1):
        """
        Get the next actions for the experiment
        trial_condition is either 1 or 0
        level can be 1 (? dB difference) or higher (smaller differences)
        """
        try:
            section = session.playlist.section_set.filter(group_id=level).get(tag_id=trial_condition)
        except Section.DoesNotExist:
            return None
        expected_result = 'in2' if trial_condition else 'in3'
        # create Result object and save expected result to database
        result_pk = Base.prepare_result(session, section, expected_result)
        instructions = {
            'preload': '',
            'during_presentation': ''
        }
        question = ChoiceQuestion(
            key='longer_or_equal',
            question=_(
                "Is the rhythm a DUPLE METER (MARCH) or a TRIPLE METER (WALTZ)?"),
            choices={
                'in2': _('DUPLE METER'),
                'in3': _('TRIPLE METER')
            },
            view='BUTTON_ARRAY',
            result_id=result_pk,
            submits=True
        )
        play_config = {
            'decision_time': section.duration + .5
        }
        playback = Playback('AUTOPLAY', [section], instructions, play_config)
        form = Form([question])
        view = Trial(
            playback=playback,
            feedback_form=form,
            title=_('Meter detection')
        )
        return view.action()

    @classmethod
    def response_explainer(cls, correct, in2, button_label=_('Next fragment')):
        if correct:
            if in2:
                instruction = _(
                    'The rhythm was a DUPLE METER. Your answer was CORRECT.')
            else:
                instruction = _(
                    'The rhythm was a TRIPLE METER. Your answer was CORRECT.')
        else:
            if in2:
                instruction = _(
                    'The rhythm was a DUPLE METER. Your answer was INCORRECT.')
            else:
                instruction = _(
                    'The rhythm was a TRIPLE METER. Your response was INCORRECT.')
        return Explainer.action(
            instruction=instruction,
            steps=[],
            button_label=button_label
        )
    
    @classmethod
    def finalize_experiment(cls, session, request_session):
        """ if either the max_turnpoints have been reached,
        or if the section couldn't be found (outlier), stop the experiment
        """
        loudness_diff = int(get_average_difference_level_based(session, 6))
        score_message = _("Well done! You heard the difference \
            when the accented tone was only {} dB louder.\n\nA march and a waltz are very common meters in Western music, but in other cultures, much more complex meters also exist!").format(loudness_diff)
        session.finish()
        session.save()
        return final_action_with_optional_button(session, score_message, request_session)

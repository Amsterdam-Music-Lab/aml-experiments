import random
import logging
import copy

from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string

from .base import Base
from .views import Trial, Explainer, Consent, StartSession, Step, Question
from .views.form import ChoiceQuestion, RangeQuestion, Form
from .views.playback import Playback
from .util.questions import question_by_key
from .util.actions import combine_actions, final_action_with_optional_button, render_feedback_trivia

logger = logging.getLogger(__name__)

class Eurovision2022(Base):
    """Rules for the beat alignment test by Mullensiefen et al. (2014)"""

    ID = 'EUROVISION_2022'

    @classmethod
    def first_round(cls, experiment):
        """Create data for the first experiment rounds"""

        # 1. General explainer
        explainer = Explainer(
            instruction=_(
                "This test measures your ability to recognize the beat in a piece of music."),
            steps=[
                Step(_(
                        "Listen to the following music fragments. In each fragment you hear a series of beeps.")),
                Step(_(
                        "It's you job to decide if the beeps are ALIGNED TO THE BEAT or NOT ALIGNED TO THE BEAT of the music.")),
                Step(_("Remember: try not to move or tap along with the sounds")),
                Step(_(
                        "Listen carefully to the following examples. Pay close attention to the description that accompanies each example."))
            ],
            button_label=_('Ok')
            ).action(True)

        # 2. Consent with rendered text (lives in templates folder)
        # rendered = render_to_string('consent_hooked.html')
        rendered = "Informed Consent"
        consent = Consent.action(rendered)

        # 3. Start session
        start_session = StartSession.action()
        return combine_actions(
            explainer,
            consent,
            start_session
        )

    @classmethod
    def next_round(cls, session, request_session=None):
        """Get action data for the next round"""

        # If the number of results equals the number of experiment.rounds
        # Close the session and return data for the final_score view
        if session.rounds_complete():
            # Finish session
            session.finish()
            session.save()
            percentage = int((sum([r.score for r in session.result_set.all()]) / session.experiment.rounds) * 100)
            feedback = _('Well done! You’ve answered {} percent correctly!').format(percentage)
            trivia = _('In the UK, over 140.000 people did \
                this test when it was first developed?')
            final_text = render_feedback_trivia(feedback, trivia)
            return final_action_with_optional_button(session, final_text, request_session)

        # Next round number, can be used to return different actions
        next_round_number = session.get_next_round()
        return cls.next_betting_action(session, next_round_number)

    @classmethod
    def next_trial_action(cls, session, this_round):
        """Get next section for given session"""
        filter_by = {'tag_id': 0}
        section = session.section_from_unused_song(filter_by)
        condition = section.filename.split('_')[-1][:-4]
        expected_result = 'ON' if condition=='on' else 'OFF'
        result_pk = Base.prepare_result(session, section, expected_result)
        question = ChoiceQuestion(
            question=_("Are the beeps ALIGNED TO THE BEAT or NOT ALIGNED TO THE BEAT?"),
            key='aligned',
            choices={
                'ON': _('ALIGNED TO THE BEAT'),
                'OFF': _('NOT ALIGNED TO THE BEAT')
            },
            view='BUTTON_ARRAY',
            result_id=result_pk,
            submits=True
        )
        form = Form([question])
        play_config = {
            'decision_time': section.duration + .1,
        }
        playback = Playback('AUTOPLAY', [section], play_config=play_config)
        view = Trial(
            playback=playback,
            feedback_form=form,
            title=_('Beat alignment'),
            config={
                'listen_first': True
            }
        )
        return view.action()

    def next_playback_action(self, session):
        """Play the next song"""
        playback = Playback('BUTTON', [section])
        view = Trial(
            playback=playback,
            feedback_form=None,
            title=_("Greece"),
            config={
                'listen_first': True
            }
        )

    def next_betting_action(self, session):
        """Get next betting action for given session"""
        available_countries = ChoiceQuestion(
            question=_("Which country would you like to bet on?"),
            key='country',
            choices={
                'Austria': _('Austria'),
                'Greece': _('Greece'),
                'Netherlands': _('Netherlands')
            },
            view='DROPDOWN',
            is_skippable=False,
            submits=False
        )
        money = RangeQuestion(
            question=_("How much money would you like to bet?"),
            key='money',
            min_value=1,
            max_value=25,
            view="RANGE"
            is_skippable=False,
            submits=False
        )
        form = Form([available_countries, money])
        view = Trial(
            playback=None,
            feedback_form=form,
            title=_('Betting')
        )
        return view.action()

    @staticmethod
    def calculate_score(result, form_element, data):
        try:
            expected_response = result.expected_response
        except Exception as e:
            logger.log(e)
            expected_response = None
        if expected_response and expected_response == form_element['value']:
            return 1
        else:
            return 0

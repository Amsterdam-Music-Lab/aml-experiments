import logging

from django.utils.translation import gettext_lazy as _
from .views import Trial, Consent, Explainer, Final, Playlist, StartSession
from .views.form import Form
from .util.goldsmiths import MSI_F3_MUSICAL_TRAINING
from .util.questions import EXTRA_DEMOGRAPHICS, question_by_key
from .util.actions import combine_actions, final_action_with_optional_button

from .base import Base


class GoldMSI(Base):
    """ an experiment view that implements the GoldMSI questionnaire """
    ID = 'GOLD_MSI'
    demographics = [
        question_by_key('dgf_gender_identity'),
        question_by_key('dgf_age', EXTRA_DEMOGRAPHICS),
        question_by_key('dgf_education', drop_choices=['isced-1']),
        question_by_key('dgf_highest_qualification_expectation',
                        EXTRA_DEMOGRAPHICS),
        question_by_key('dgf_country_of_residence'),
        question_by_key('dgf_country_of_origin'),
    ]
    questions = MSI_F3_MUSICAL_TRAINING + demographics

    @classmethod
    def first_round(cls, experiment, participant):
        consent = Consent.action()
        start_session = StartSession.action()
        return [
            consent,
            start_session
        ]

    @classmethod
    def next_round(cls, session, request_session=None):
        round_number = session.total_questions()
        if round_number == len(cls.questions):
            return final_action_with_optional_button(session, '', request_session)
        question = cls.questions[round_number]
        cls.prepare_profile(session.participant, question.key, question.scoring_rule)
        feedback_form = Form([
            question,
        ], is_profile=True)
        view = Trial(None, feedback_form)
        return view.action()

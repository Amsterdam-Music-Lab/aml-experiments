import numpy as np

from django.utils.translation import gettext as _
from django.template.loader import render_to_string

from .base import Base

from experiment.actions import Consent, Explainer, Step, Final, Playlist, Trial, StartSession
from experiment.actions.form import Form, RadiosQuestion
from experiment.actions.playback import Playback
from experiment.questions.demographics import EXTRA_DEMOGRAPHICS
from experiment.questions.languages import LANGUAGE, LanguageQuestion
from experiment.questions.utils import question_by_key

from result.utils import prepare_result

n_representations = 8
n_trials_per_block = 8
n_rounds_per_block = n_trials_per_block * 2  # each trial has two rounds


class Speech2Song(Base):
    """ Rules for a speech-to-song experiment """
    ID = 'SPEECH_TO_SONG'
    
    def __init__(self):
        self.questions = [
            question_by_key('dgf_age', EXTRA_DEMOGRAPHICS),
            question_by_key('dgf_gender_identity'),
            question_by_key('dgf_country_of_origin_open', EXTRA_DEMOGRAPHICS),
            question_by_key('dgf_country_of_residence_open', EXTRA_DEMOGRAPHICS),
            question_by_key('lang_mother', LANGUAGE),
            question_by_key('lang_second', LANGUAGE),
            question_by_key('lang_third', LANGUAGE),
            LanguageQuestion(_('English')).exposure_question(),
            LanguageQuestion(_('Brazilian Portuguese')).exposure_question(),
            LanguageQuestion(_('Mandarin Chinese')).exposure_question()
        ]

    def first_round(self, experiment):
        explainer = Explainer(
            instruction=_("This is an experiment about an auditory illusion."),
            steps=[
                Step(
                    description=_("Please wear headphones (earphones) during the experiment to maximise the experience of the illusion, if possible.")
                )
            ],
            button_label=_('Start')
        )
        # read consent form from file
        rendered = render_to_string(
            'consent/consent_speech2song.html')

        consent = Consent(
            rendered, title=_('Informed consent'), confirm=_('I agree'), deny=_('Stop'))

        playlist = Playlist(experiment.playlists.all())

        start_session = StartSession()

        return [
            explainer,
            consent,
            playlist,
            start_session
        ]

    def next_round(self, session):
        blocks = [1, 2, 3]
        # shuffle blocks based on session.id as seed -> always same order for same session
        np.random.seed(session.id)
        np.random.shuffle(blocks)
        # group_ids for practice (0), or one of the speech blocks (1-3)
        actions = []
        is_speech = True
        if session.current_round == 1:
            question_trial = self.get_questionnaire(session)
            if question_trial:
                return question_trial

            explainer = Explainer(
                instruction=_(
                    'Thank you for answering these questions about your background!'),
                steps=[
                    Step(
                        description=_(
                            'Now you will hear a sound repeated multiple times.')
                    ),
                    Step(
                        description=_(
                            'Please listen to the following segment carefully, if possible with headphones.')
                    ),
                ],
                button_label=_('OK')
            )
            return [
                explainer,
                *next_repeated_representation(session, is_speech, 0)
            ]
        if session.current_round == 2:
            e1 = Explainer(
                instruction=_('Previous studies have shown that many people perceive the segment you just heard as song-like after repetition, but it is no problem if you do not share that perception because there is a wide range of individual differences.'),
                steps=[],
                button_label=_('Continue')
            )
            e2 = Explainer(
                instruction=_('Part 1'),
                steps=[
                    Step(
                        description=_('In the first part of the experiment, you will be presented with speech segments like the one just now in different languages which you may or may not speak.')),
                    Step(
                        description=_('Your task is to rate each segment on a scale from 1 to 5.'))
                ],
                button_label=_('Continue')
            )
            actions.extend([e1, e2])
            group_id = blocks[0]
        elif 2 < session.current_round <= n_rounds_per_block + 1:
            group_id = blocks[0]
        elif n_rounds_per_block + 1 < session.current_round <= 2 * n_rounds_per_block + 1:
            group_id = blocks[1]
        elif 2 * n_rounds_per_block + 1 < session.current_round <= 3 * n_rounds_per_block + 1:
            group_id = blocks[2]
        elif session.current_round == 3 * n_rounds_per_block + 2:
            # Final block (environmental sounds)
            e3 = Explainer(
                instruction=_('Part2'),
                steps=[
                    Step(
                        description=_(
                            'In the following part of the experiment, you will be presented with segments of environmental sounds as opposed to speech sounds.')
                    ),
                    Step(
                        description=_('Environmental sounds are sounds that are not speech nor music.')
                    ),
                    Step(
                        description=_('Like the speech segments, your task is to rate each segment on a scale from 1 to 5.')
                    )
                ],
                button_label=_('Continue')
            )
            actions.append(e3)
            group_id = 4
            is_speech = False
        elif 3 * n_rounds_per_block + 2 < session.current_round <= 4 * n_rounds_per_block + 1:
            group_id = 4
            is_speech = False
        else:
            # Finish session
            session.finish()
            session.save()
            # Return a score and final score action
            return Final(
                title=_('End of experiment'),
                session=session,
                score_message=_(
                    'Thank you for contributing your time to science!')
            )
        if session.current_round % 2 == 0:
            # even round: single representation (first round are questions only)
            actions.extend(next_single_representation(
                session, is_speech, group_id))
        else:
            # uneven round: repeated representation
            actions.extend(next_repeated_representation(
                session, is_speech))
        return actions


def next_single_representation(session, is_speech, group_id):
    """ combine a question after the first representation,
    and several repeated representations of the sound,
    with a final question"""
    filter_by = {'group': group_id}
    section = session.section_from_unused_song(filter_by)
    actions = [sound(section), speech_or_sound_question(session, section, is_speech)]
    return actions


def next_repeated_representation(session, is_speech, group_id=-1):
    if group_id >= 0:
        # for the Test case, there is no previous section to look at
        section = session.playlist.section_set.get(group=group_id)
    else:
        section = session.previous_section()
    actions = [sound(section, i) for i in range(1, n_representations+1)]
    actions.append(speech_or_sound_question(session, section, is_speech))
    return actions


def speech_or_sound_question(session, section, is_speech):
    if is_speech:
        question = question_speech(session, section)
    else:
        question = question_sound(session, section)
    return Trial(playback=None, feedback_form=Form([question]))


def question_speech(session, section):
    key = 'speech2song'
    return RadiosQuestion(
        key=key,
        question=_('Does this sound like song or speech to you?'),
        choices=[
            _('sounds exactly like speech'),
            _('sounds somewhat like speech'),
            _('sounds neither like speech nor like song'),
            _('sounds somewhat like song'),
            _('sounds exactly like song')],
        result_id=prepare_result(key, session, section=section, scoring_rule='LIKERT')
    )


def question_sound(session, section):
    key = 'sound2music'
    return RadiosQuestion(
        key=key,
        question=_(
            'Does this sound like music or an environmental sound to you?'),
        choices=[
            _('sounds exactly like an environmental sound'),
            _('sounds somewhat like an environmental sound'),
            _('sounds neither like an environmental sound nor like music'),
            _('sounds somewhat like music'),
            _('sounds exactly like music')],
        result_id=prepare_result(key, session, section=section, scoring_rule='LIKERT'),
    )


def sound(section, n_representation=None):
    if n_representation and n_representation > 1:
        ready_time = 0
    else:
        ready_time = 1
    config = {
        'ready_time': ready_time,
        'show_animation': False
    }
    title = _('Listen carefully')
    playback = Playback(
        sections = [section],
        player_type='AUTOPLAY',
        play_config=config
    )
    view = Trial(
            playback=playback,
            feedback_form=None,
            title=title,
            config={
                'auto_advance': True,
                'show_continue_button': False,
                'response_time': section.duration+.5}
    )

    return view

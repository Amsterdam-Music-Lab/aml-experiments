from os.path import join
from django.template.loader import render_to_string
from .toontjehoger_1_mozart import toontjehoger_ranks
from experiment.actions import Explainer, Step, Final, Info
from experiment.actions.utils import get_current_experiment_url
from .toontjehoger_4_absolute import ToontjeHoger4Absolute


class ToontjeHogerKids4Absolute(ToontjeHoger4Absolute):
    ID = 'TOONTJE_HOGER_KIDS_4_ABSOLUTE'
    PLAYLIST_ITEMS = 12

    def first_round(self, block):
        """Create data for the first block rounds."""

        # 1. Explain game.
        explainer = Explainer(
            instruction="Absoluut gehoor",
            steps=[
                Step(
                    "Je hoort straks stukjes muziek van televisie of filmpjes."),
                Step(
                    "Het zijn er steeds twee: Eentje is het origineel, de andere hebben we een beetje hoger of lager gemaakt."),
                Step("Welke klinkt precies zoals jij 'm kent? Welke is het origineel?"),
            ],
            step_numbers=True,
            button_label="Start"
        )

        return [
            explainer,
        ]

    def get_trial_question(self):
        return "Welke van deze twee stukjes muziek klinkt precies zo hoog of laag als jij 'm kent?"

    def get_final_round(self, session):

        # Finish session.
        session.finish()
        session.save()

        # Score
        score = self.get_score(session)

        # Final
        final_text = "Best lastig!"
        if session.final_score >= session.block.rounds * 0.5 * self.SCORE_CORRECT:
            final_text = "Goed gedaan!"

        final = Final(
            session=session,
            final_text=final_text,
            rank=toontjehoger_ranks(session),
            button={'text': 'Wat hebben we getest?'}
        )

        # Info page
        debrief_message = "Lukte het jou om het juiste antwoord te kiezen? Dan heb je goed onthouden hoe hoog of laag die muziekjes normaal altijd klinken! Sommige mensen noemen dit absoluut gehoor. \
            Is dat eigenlijk bijzonder? Kijk de filmpjes om daar achter te komen!"
        body = render_to_string(
            join('info', 'toontjehogerkids', 'debrief.html'),
            {'debrief': debrief_message,
             'vid1': 'https://www.youtube.com/embed/AkbIazK9Jcc?si=yjJLjXQa8wQbvSrf',
             'vid2': 'https://www.youtube.com/embed/KVB6d0Oy_5o?si=zxj1gUzjME_n-fQ5'})
        info = Info(
            body=body,
            heading="Absoluut gehoor",
            button_label="Terug naar ToontjeHogerKids",
            button_link=get_current_experiment_url(session)
        )

        return [*score, final, info]

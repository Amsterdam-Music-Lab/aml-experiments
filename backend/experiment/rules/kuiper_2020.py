import random
from django.utils.translation import gettext_lazy as _

from section.models import Section
from session.models import Session
from .hooked import Hooked


class Kuiper2020(Hooked):
    """Rules for the Christmas version of the Hooked experiment.

    Based on the MBCS internship projects of Leanne Kuiper.
    """

    ID = 'KUIPER_2020'

    def select_song_sync_section(self, session: Session, condition) -> Section:
        if condition == 'returning':
            return session.playlist.get_section({'tag__gt': 0},
                                                song_ids=session.get_unused_song_ids({'tag__gt': 0}))
        else:
            return session.playlist.get_section(song_ids=session.get_unused_song_ids())

    def select_heard_before_section(self, session: Session, condition: str) -> Section:
        session_type = self.get_session_type(session)
        if session_type == 'same':
            return super().select_heard_before_section(session, condition)
        else:
            current_section_id = self.get_current_section_id(session)
            played_section = Section.objects.get(pk=current_section_id)
            allowed_tags = ['0', '1', '2', '3']
            allowed_tags.remove(played_section.tag)
            return session.playlist.get_section({'song__id': played_section.song.id, 'tag__in': allowed_tags})

    def get_session_type(self, session):
        random.seed(session.id)
        return random.choice(['same', 'different'])

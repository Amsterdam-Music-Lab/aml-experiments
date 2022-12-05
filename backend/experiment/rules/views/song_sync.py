import math
import random

from django.utils.translation import gettext_lazy as _

class SongSync(object):  # pylint: disable=too-few-public-methods
    """
    Provide data for a SongSync view that handles views for song recognition,
    a silence and in- or out-sync continuation of audio playback
    """
    ID = 'SONG_SYNC'

    def __init__(self, section, result_id, title=None, config=None, scoring_rule=None, instructions=None, buttons=None):
        '''
        initialize SongSync, with the following arguments:
        - section: section to be played during the round
        - title: title of the page
        - config: optional settings to override the default config
        - instructions: optional instructions to override the default instructions
        - buttons: optional button labels to override the default labels
        '''
        self.section = section
        self.result_id = result_id
        self.scoring_rule = scoring_rule
        continuation_correctness = random.randint(0, 1) == 1
        self.config = {
            'ready_time': 3,
            'recognition_time': 15,
            'silence_time': 4,
            'sync_time': 15,
            'continuation_offset': random.randint(100, 150) / 10 if not continuation_correctness else 0,
            'continuation_correctness': continuation_correctness,
        }
        if config:
            self.config.update(config)
        self.instructions = {
            'recognize': _('Do you recognise this song?'),
            'imagine': _('Keep imagining the music'),
            'correct': _('Did the track come back in the right place?'),
            'ready': _('Get ready!')
        }
        if instructions:
            self.instructions.update(instructions)
        self.buttons = {
            'yes': _('Yes'),
            'no': _('No')
        }
        self.title = title
        if buttons:
            self.buttons.update(buttons)

    def action(self):
        """Serialize data for song_sync action"""
        # Create action
        action = {
            'view': self.ID,
            'section': self.section.absolute_url(),
            'resultId': self.result_id,
            'scoring_rule': self.scoring_rule,
            'config': self.config,
            'title': self.title,
            'instructions': self.instructions,
            'buttons': self.buttons,
        }

        return action

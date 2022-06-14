import random

from django.utils.translation import gettext as _

class Score(object):  # pylint: disable=too-few-public-methods
    """
    Provide data for an intermediate score view

    Relates to client component: Score.js 
    """

    ID = 'SCORE'

    def __init__(self, session, score_message=None, config=None, icon=None):
        """ Score presents feedback to a participant after a Trial
        - session: a Session object
        - score_message: a function which constructs feedback text based on the score
        - config: a dict with the following settings:
            - timer: int or None. If defined, advance to next view after n seconds
            - show_section: whether metadata of the section should be shown
            - show_total_score: whether the total score should be shown
        - icon: the name of a themify-icon shown with the view or None
        """
        self.session = session
        self.score = session.last_score()
        self.score_message = score_message or self.default_score_message
        self.config = {
            'timer': None,
            'show_section': False,
            'show_total_score': False
        }
        if config:
            self.config.update(config)
        self.icon = icon
        self.texts = {
            'score': _('Score'),
            'next': _('Next'),
            'listen_explainer': _('You listened to:')
        }

    def action(self):
        """Serialize score data"""
        
        # Create action
        action = {
            'view': self.ID,
            'title': _('Round {} / {}').format(
                self.session.rounds_passed(), self.session.experiment.rounds),
            'score': self.score,
            'score_message': self.score_message(self.score),
            'total_score': self.session.total_score(),
            'texts': self.texts,
            'icon': self.icon
        }
        if self.config.get('show_section'):
            action['last_song'] = self.session.last_song()
        return action

    def default_score_message(self, score):
        """Fallback to generate a message for the given score"""
        # Zero
        if score == 0:
            # "Too bad!", "Come on!", "Try another!", "Try again!"
            return random.choice([_("No points")])
        # Negative
        if score < 0:
            return random.choice([_("Incorrect")])  # "Too bad!", "Fail!", "Nooo!"
        # Positive
        # "Well done!", "Nice job!", "Great one!", "Score!", "You're good!", "Awesome!", "Nice one!"
        return random.choice([_("Correct")])

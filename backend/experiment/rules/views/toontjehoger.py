class ToontjeHoger:  # pylint: disable=too-few-public-methods
    """
    Provide data for a view that shows the ToontjeHoger homepage

    Relates to client component: ToontjeHoger.js
    """

    ID = "TOONTJEHOGER"

    def __init__(self,config, experiments = []):
        """
        ToontjeHoger shows the ToontjeHoger homepage
        
        config: Object containing texts and other configuration
            - payoff
            - intro
            - main_button_label
            - main_button_url
            - supporters_intro
        experiments: A list of ExperimentData objects
        """
        self.config = config
        self.experiments = experiments

    def action(self):
        """Get data for ToontjeHoger action"""

        return {
            'view': ToontjeHoger.ID,
            'config': self.config,
            'experiments': [vars(i) for i in self.experiments]
        }


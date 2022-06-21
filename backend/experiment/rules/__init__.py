from .beat_alignment import BeatAlignment
from .speech2song import Speech2Song
from .duration_discrimination import DurationDiscrimination
from .duration_discrimination_tone import DurationDiscriminationTone
from .anisochrony import Anisochrony
from .h_bat import HBat
from .h_bat_bfit import HBatBFIT
from .hbat_bst import BST
from .rhythm_discrimination import RhythmDiscrimination
from .rhythm_experiment_series import RhythmExperimentSeries
from .rhythm_experiment_series_mri import RhythmExperimentSeriesMRI
from .gold_msi import GoldMSI
from .listening_conditions import ListeningConditions
from .hooked import Hooked
from .categorization import Categorization

# Rules available to this application
# If you create new Rules, add them to the list
# so they can be referred to by the admin

EXPERIMENT_RULES = {
    BeatAlignment.ID: BeatAlignment,
    Speech2Song.ID: Speech2Song,
    DurationDiscrimination.ID: DurationDiscrimination,
    DurationDiscriminationTone.ID: DurationDiscriminationTone,
    Anisochrony.ID: Anisochrony,
    HBat.ID: HBat,
    HBatBFIT.ID: HBatBFIT,
    BST.ID: BST,
    RhythmDiscrimination.ID: RhythmDiscrimination,
    RhythmExperimentSeries.ID: RhythmExperimentSeries,
    RhythmExperimentSeriesMRI.ID: RhythmExperimentSeriesMRI,
    GoldMSI.ID: GoldMSI,
    ListeningConditions.ID: ListeningConditions,
    Hooked.ID: Hooked,
    Categorization.ID: Categorization,
}

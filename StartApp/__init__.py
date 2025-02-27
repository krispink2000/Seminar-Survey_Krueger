from otree.api import (
    Page,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    models,
    widgets,
)
import custom_python.get_config as cf
import custom_python.quota_calc as quota

doc = """
StartApp contains a welcome page and a preparation questionnaire.
"""

class C(BaseConstants):
    NAME_IN_URL = "StartApp"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

class Subsession(BaseSubsession):
    pass

def creating_session(subsession):
    # Create quota group counts
    for count in range(len(cf.prep_gender_ch) - 1):
        subsession.session.vars[f"completed_gender_{count}"] = 0
    for count in range(len(cf.age_groups)):
        subsession.session.vars[f"completed_age_group_{count}"] = 0
    for count in range(len(cf.prep_federal_state_ch) - 1):
        subsession.session.vars[f"completed_federal_state_{count}"] = 0
    del count

class Group(BaseGroup):
    pass


# PLAYER / VARIABLES
class Player(BasePlayer):

    prep_gender = models.IntegerField(
        label=cf.prep_gender_lb,
        choices=cf.prep_gender_ch,
        widget=widgets.RadioSelect,
    )
    prep_age = models.IntegerField(min=1900, max=2025, label=cf.prep_age_lb)

    prep_eligible = models.IntegerField(
        label=cf.prep_eligible_lb,
        choices=cf.prep_eligible_ch,
        widget=widgets.RadioSelect,
    )

    prep_participation = models.IntegerField(
        blank=True,  # doesn't need to be checked to continue
        label=cf.prep_participation_lb,
        choices=cf.prep_participation_ch,
        widget=widgets.RadioSelect,
    )

    prep_federal_state = models.IntegerField(
        blank=True,  # doesn't need to be checked to continue
        label=cf.prep_federal_state_lb,
        choices=cf.prep_federal_state_ch,
        widget=widgets.RadioSelect,
    )

    browser_type = models.StringField(blank=True)
    device_type = models.StringField(blank=True)
    os_system = models.StringField(blank=True)


# PAGES
class Welcome(Page):
    name = "welcome"
    form_model = Player
    #form_fields = ["browser_type", "device_type", "os_system"] #thought this might fix it

    @classmethod
    def live_method(cls, player, data):
        if data.get("browser_type"):
            player.browser_type = data["browser_type"]
            player.device_type = data["device_type"]
            player.os_system = data["os_system"]
        return super().live_method(player, data)


class Screening(Page):
    name = "screen"
    form_model = Player

    @staticmethod
    def get_form_fields(player):
        form_fields = [
            "prep_gender",
            "prep_age",
            "prep_eligible",
            "prep_participation",
            "prep_federal_state",
        ]
        return form_fields

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.session.config["quota_screenout"]:
            quota.filtering(player)

        # saving some fields in the participant model to be able to access these
        # values in other apps
        player.participant.federal_state = player.field_maybe_none(
            "prep_federal_state"
        )
        player.participant.eligible = player.prep_eligible
        player.participant.gender = player.prep_gender
    
    
page_sequence = [Welcome, Screening]

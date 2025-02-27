from otree.api import (
    BaseConstants,
    Page,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    models,
    Page,
    widgets,
)
import custom_python.get_config as cf
import custom_python.quota_calc as quota

doc = """
EndApp contains additional questions and an end page which redirects.
"""

class C(BaseConstants):
    NAME_IN_URL = "EndApp"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass

pages = [
    "ideology"
    "edu",
    "income",
    "end",
]

# PLAYER / VARIABLES
class Player(BasePlayer):
    
    ### Ideology ###
    left_right_ideology =  models.IntegerField(blank=True, max=11, min=1, label="")

    ### Education ###
    edu_general_education = models.IntegerField(
        widget=widgets.RadioSelect,
        choices=cf.edu_general_education_ch,
        label=cf.edu_general_education_lb,
        blank=True,
    )
    edu_general_education_open = models.StringField(label="", blank=True)
    edu_vocational_training = models.IntegerField(
        widget=widgets.RadioSelect,
        choices=cf.edu_vocational_training_ch,
        label=cf.edu_vocational_training_lb,
        blank=True,
    )
    edu_vocational_training_open = models.StringField(label="", blank=True)

    ### Income ###
    income_net_income = models.IntegerField(
        widget=widgets.RadioSelect,
        choices=cf.income_net_income_ch,
        label=cf.income_net_income_lb,
        blank=True,
    )

# PAGES

### Ideology ###
class Ideology (Page):
    name = "ideology"
    form_model = Player

    form_fields = [
        "left_right_ideology",
    ]

### Education ###
class Education(Page):
    name = "edu"
    form_model = Player

    form_fields = [
        "edu_general_education",
        "edu_general_education_open",
        "edu_vocational_training",
        "edu_vocational_training_open",
    ]


### Income ###
class Income(Page):
    name = "income"
    form_model = Player
    form_fields = ["income_net_income"]


### End_Page ###
class End(Page):
    name = "end"
    form_model = Player

    @classmethod
    def before_next_page(cls, player, timeout_happened):
        # Having finished the survey, the player is counted towards the quota
        quota.counting(player)


class Redirect(Page):
    form_model = Player
    @staticmethod
    def is_displayed(player):
        return player.session.config["quota_screenout"]

    @staticmethod
    def js_vars(player):
        return dict(
            # getting redirect link from settings.py
            link=player.session.config["normal_redirect_link"]
            + str(player.participant.label),
        )


page_sequence = [
    Ideology,
    Education,
    Income,
    End,
    Redirect,
]

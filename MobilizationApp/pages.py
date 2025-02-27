from otree.api import Currency as c, currency_range, safe_json
from otree.api import Currency as c, currency_range
from custom_python.redirecting import ScreenoutPage
from ._builtin import Page, WaitPage
from .models import Constants, Player
from . import *
import random


class Welcome(Page):
    form_model = Player
    form_fields = ['time_start']
     
        
    def vars_for_template(self):
        return {
            "participant_label": self.participant.label
        }   
    
    def before_next_page(self):
        treatments = ['positive_prognostic', 
                'positive_diagnostic', 
                'negative_prognostic', 
                'negative_diagnostic']
        
        self.participant.vars['assigned_treatment'] = random.choice(treatments)
        self.player.treatment = self.participant.vars['assigned_treatment']

class PreTreatment(Page):
    form_model = Player
    form_fields = ['eco_poli_affiliation', 
                   'soci_poli_affiliation']
    

class PreTreatment2(Page):
    form_model = Player
    form_fields = ['concept_freetrade', 
                   'mercosur_freetrade', 
                   'supportive_freetrade',
                   'political_stance_trade', 
                   'trust_institutions', 
                   'interest_politics']
    
class PreTreatment3(Page):
    form_model = Player
    form_fields = ['pre_talk_friends',
                   'pre_share_socialmedia',
                   'pre_consider_voting',
                   'pre_support_petition',
                   'pre_attend_protest',
                   'pre_legal_action',
                   'pre_last_vote',
                   'pre_contact_politics',
                   'pre_boycott']


class FramingTreatment(Page):
    form_model = Player
    form_fields = ['time_popout', 'select_proceed']
    
    def vars_for_template(self):
        return {'ass_treatment': self.player.treatment} 

    

class ManipulationCheck(Page):
    form_model = Player
    form_fields = ['overall_tone',
                   'impact_time']

class PostTreatment(Page):
    form_model = Player
    form_fields = ['post_talk_friends',
                    'post_share_socialmedia',
                    'post_consider_voting',
                    'post_support_petition',
                    'post_attend_protest',
                    'post_legal_action',
                    'post_next_vote',
                    'post_contact_politics',
                    'post_boycott']
    
class PostTreatment2(Page):
    form_model = Player
    form_fields = [ 'supportive_mercosur',
                    'convincing_arguments',
                    'important_mercosur_state',
                    'important_mercosur_you']

#Here we define in which ordering we want the pages to be shown. We always start with a Welcome page and end with an End page.
page_sequence = [Welcome,
                PreTreatment,
                PreTreatment2,
                PreTreatment3,
                FramingTreatment,
                PostTreatment,
                PostTreatment2,
                ManipulationCheck]

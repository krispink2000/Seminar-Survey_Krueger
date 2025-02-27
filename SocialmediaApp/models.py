from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)

import json

from otree.forms.widgets import CheckboxInput
from datetime import datetime

class Constants(BaseConstants):
    name_in_url = 'FakeNews'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    #Pre-Questions
    mediasource_social = models.BooleanField(widget=CheckboxInput, blank=True)
    mediasource_online = models.BooleanField(widget=CheckboxInput, blank=True)
    mediasource_printed = models.BooleanField(widget=CheckboxInput, blank=True)
    mediasource_tv = models.BooleanField(widget=CheckboxInput, blank=True)
    mediasource_radio = models.BooleanField(widget=CheckboxInput, blank=True)
    mediasource_other = models.StringField(blank=True)
    mediasource_none = models.IntegerField(blank=True)

    social_media = models.IntegerField(label='Social Media Question')
    socialmedia_facebook = models.BooleanField(widget=CheckboxInput, blank=True)
    socialmedia_twitter = models.BooleanField(widget=CheckboxInput, blank=True)
    socialmedia_instagram = models.BooleanField(widget=CheckboxInput, blank=True)
    socialmedia_tiktok = models.BooleanField(widget=CheckboxInput, blank=True)
    socialmedia_linkedin = models.BooleanField(widget=CheckboxInput, blank=True)
    socialmedia_xing = models.BooleanField(widget=CheckboxInput, blank=True)
    socialmedia_none = models.IntegerField(blank=True)
    socialmedia_other = models.StringField(blank=True)
    
    
    #Post-Questions
    post_quest = models.IntegerField(label='End Question', blank=False)
    post_quest_2 = models.IntegerField(label='End Question', blank=False)
    post_quest_3 = models.IntegerField(label='End Question', blank=False)
    
    # TweetsPage
    tweet_index = models.IntegerField(initial=0)
    content_index = models.IntegerField(initial=0)
    community_index = models.IntegerField(initial=0)
    
    
    # Time variables
    tweet_page_times = models.LongStringField(initial="[]")
    content_page_times = models.LongStringField(initial="[]")
    
    
    # Content display related variables
    show_notfake_tweet = models.BooleanField(initial=True)
    show_notfake_content = models.BooleanField(initial=True)
    
    show_note_index = models.IntegerField(initial=0)
    note_display_order = models.StringField(initial="[]")
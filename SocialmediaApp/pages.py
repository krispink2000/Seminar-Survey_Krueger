from otree.api import Currency as c, currency_range, safe_json
from ._builtin import Page, WaitPage
from custom_python.redirecting import ScreenoutPage
from .models import Constants, Player

import os
import json
import random

from datetime import datetime
    
    
## open json functions ##
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_json_data(filename):
    json_path = os.path.join(BASE_DIR, '_static', 'texts', filename)
    with open(json_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def load_all_data():
    tweets = load_json_data('tweets.json')
    content = load_json_data('content.json')
    community = load_json_data('community_notes.json')
    
    return {
        'tweets': tweets,
        'content': content,
        'community': community
    }


## Pages ##
class PreQuestionsPage(ScreenoutPage):
    form_model = Player
    form_fields = ['mediasource_social', 'mediasource_online', 'mediasource_printed', 'mediasource_tv', 'mediasource_radio', 'mediasource_none',
                   'social_media',
                   'socialmedia_facebook', 'socialmedia_twitter', 'socialmedia_other', 'socialmedia_instagram', 'socialmedia_tiktok', 'socialmedia_linkedin', 'mediasource_other', 'socialmedia_xing', 'socialmedia_none']


class IntroPage(ScreenoutPage):
    form_model = Player


class TweetsPage(Page):
    form_model = Player
    
    def before_next_page(self):
        # Timestamp
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        times = json.loads(self.player.tweet_page_times)
        times.append(current_time)

        self.player.tweet_page_times = json.dumps(times)

        # Order of tweets and community notes
        self.player.show_notfake_tweet = not self.player.show_notfake_tweet
        
        if self.player.show_notfake_tweet:
            self.player.tweet_index += 1
            self.player.community_index += 1
        else: 
            self.player.tweet_index -= 0
            self.player.community_index -= 0
            
        # Indexing for the shown notes
        self.player.show_note_index += 1
        
    
    def vars_for_template(self):
        data = load_all_data()

        # Load in function for the tweets and community notes
        tweet_index = self.player.tweet_index
        community_index = self.player.community_index

        fake_tweet = data['tweets']['fake'][str(tweet_index + 1)]
        not_fake_tweet = data['tweets']['not_fake'][str(tweet_index + 1)]
     
        community_fake = data['community']['fake'][str(community_index + 1)]
        community_not_fake = data['community']['not_fake'][str(community_index + 1)]
        
        # if logic for the fake and not fake sequence
        if self.player.show_notfake_tweet:
            selected_tweet = not_fake_tweet
            selected_community = community_not_fake
        else:
            selected_tweet = fake_tweet
            selected_community = community_fake
        
        # Randomization of the shown community notes
        if not self.player.note_display_order or self.player.note_display_order == "[]":
            note_display_order = [True, True, True, False, False, False]
            random.shuffle(note_display_order)
            self.player.note_display_order = json.dumps(note_display_order)

        note_display_order = json.loads(self.player.note_display_order)
        show_note = note_display_order[self.player.show_note_index]
        
        return {
            'show_note': show_note,
            'selected_tweet': selected_tweet,
            'selected_community': selected_community
        }
    
    
class ContentPage(Page):
    form_model = Player
    
    def before_next_page(self):
        # Timestamp
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        times = json.loads(self.player.content_page_times)
        times.append(current_time)

        self.player.content_page_times = json.dumps(times)
        
        # Order of the contents
        self.player.show_notfake_content = not self.player.show_notfake_content
        
        if self.player.show_notfake_content:
            self.player.content_index += 1
        else: 
            self.player.content_index -= 0
        
        
    def vars_for_template(self):
        data = load_all_data()

        # Load in function for the contents
        content_index = self.player.content_index
        
        fake_content = data['content']['fake'][str(content_index + 1)]
        not_fake_content = data['content']['not_fake'][str(content_index + 1)]
        
        # if logic for the fake and not fake sequence
        if self.player.show_notfake_content:
            selected_content = not_fake_content
        else:
            selected_content = fake_content

        return {
            'selected_content': selected_content
        }    


class PostQuestionsPage(Page):
    form_model = Player
    form_fields = ['post_quest', 'post_quest_2', 'post_quest_3']


## Page sequence ##
page_sequence = [PreQuestionsPage, IntroPage]

for _ in range(6):
    page_sequence.append(TweetsPage)
    page_sequence.append(ContentPage)

page_sequence.append(PostQuestionsPage)
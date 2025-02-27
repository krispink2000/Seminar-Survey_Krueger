from otree.api import Page

class ScreenoutPage(Page):
    form_model = "player"
    
    def js_vars(self) -> dict:
        player = self.player  # Access the player object directly
        label = str(player.participant.label)  # Access participant through player
        if player.participant.screen_out:
            link = player.session.config["screen_out_redirect_link"] + label
        elif player.participant.quota:
            link = player.session.config["quota_redirect_link"] + label
        else:
            link = ""
        return super().js_vars() | dict(link=link)
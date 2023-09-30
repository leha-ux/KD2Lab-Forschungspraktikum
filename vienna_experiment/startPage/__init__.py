from otree.api import *

c = Currency

doc = """
Eine Startseite für ein otree Experiment, das auf einen Call des Clients wartet und dabei einen String übergeben bekommt
"""

class Constants(BaseConstants):
    name_in_url = 'startseite'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # ein Feld, um den übergebenen String zu speichern
    mappingID = models.StringField()
    

# PAGES
class StartPage(Page):
    # diese Methode wird aufgerufen, wenn der Client die Seite aufruft
    @staticmethod
    def live_method(player: Player, data):
        # data ist ein Dictionary, das die Daten enthält, die vom Client gesendet wurden
        # wir speichern den übergebenen String in dem Feld des Spielers
        player.mappingID = data['string']
        #in the game where you define the mappingID
        player.participant.vars['mappingID'] = player.mappingID 
        #store the mappingID in the participant.vars dictionary

        # wir senden eine Nachricht an alle Spieler in der Subsession, dass wir den String erhalten haben
        return {p.id_in_group: 'String erhalten' for p in player.subsession.get_players()}

class Download(Page):
    
    pass

page_sequence = [StartPage]

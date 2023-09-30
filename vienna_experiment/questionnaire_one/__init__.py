from otree.api import *
from settings import PARTICIPANT_FIELDS

doc = """
"""

class C(BaseConstants):
    NAME_IN_URL = 'questionnaire_one'
    PLAYERS_PER_GROUP = None
    INSTRUCTIONS_TEMPLATE = 'questionnaire_one.html'
    NUM_ROUNDS = 1

class Subsession(BaseSubsession):
    None


class Group(BaseGroup):
    None 

class Player(BasePlayer):
    questionaireone = models.BooleanField(
        choices=[
        [False, '5 von 50 Würfen'], 
        [False, '25 von von 50 Würfen'], 
        [True, '30 von von 50 Würfen'],
        [False, 'Keiner der oben genannten Antworten']
        ],
        label= 'Stellen Sie sich vor, Sie würfeln 50 Mal mit einem fünfseitigen Würfel. Wie oft würde dieser fünfseitige Würfel bei diesen 50 Würfen im Durchschnitt eine ungerade Zahl (1, 3 oder 5) anzeigen?', 
        widget=widgets.RadioSelect
    )
    questionairetwo = models.BooleanField(
        choices=[
        [False, '10%'], 
        [True, '25%'], 
        [False, '40%'],
        [False, 'Keiner der oben genannten Antworten']
        ],
        label= 'Von 1.000 Einwohnern einer Kleinstadt sind 500 Mitglieder in einem Chor. Von diesen 500 Chormitgliedern sind 100 Männer. Von den 500 Einwohnern, die nicht im Chor sind, sind 300 Männer. Wie groß ist die Wahrscheinlichkeit, dass ein zufällig gezogener Mann Mitglied des Chores ist? Bitte geben Sie die Wahrscheinlichkeit in Prozent an.', 
        widget=widgets.RadioSelect
    )
    questionairethree = models.BooleanField(
        choices=[
        [False, '20 von 70 Würfen'], 
        [False, '23 von of 70 Würfen'], 
        [True, '35 von  70 Würfen'],
        [False, 'Keiner der oben genannten Antworten']
        ],
        label= 'Stellen Sie sich vor, Sie werfen einen geladenen Würfel (6 Seiten). Die Wahrscheinlichkeit, dass der Würfel eine 6 zeigt, ist doppelt so hoch wie die Wahrscheinlichkeit für jede der anderen Zahlen. Wie oft würde der Würfel bei diesen 70 Würfen im Durchschnitt die Zahl 6 zeigen?', 
        widget=widgets.RadioSelect
    )
    questionairefour = models.BooleanField(
        choices=[
        [False, '4%'], 
        [True, '20%'], 
        [False, '50%'],
        [False, 'Keiner der oben genannten Antworten']
        ],
        label= 'In einem Wald sind 20% der Pilze rot, 50% braun und 30% weiß. Ein roter Pilz ist mit einer Wahrscheinlichkeit von 20% giftig. Ein nicht roter Pilz ist mit einer Wahrscheinlichkeit von 5% giftig. Wie hoch ist die Wahrscheinlichkeit, dass ein giftiger Pilz im Wald rot ist?', 
        widget=widgets.RadioSelect
    )
  
# FUNCTIONS    

# PAGES
class Quesionaire_one(Page):
    form_model = 'player'
    form_fields = ['questionaireone', 'questionairetwo','questionairethree', 'questionairefour' ]


page_sequence = [Quesionaire_one]


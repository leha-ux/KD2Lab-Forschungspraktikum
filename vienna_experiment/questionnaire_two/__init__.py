from otree.api import *
from settings import PARTICIPANT_FIELDS

doc = """
"""

class C(BaseConstants):
    NAME_IN_URL = 'questionnaire_two'
    PLAYERS_PER_GROUP = None
    INSTRUCTIONS_TEMPLATE = 'questionnaire_two.html'
    NUM_ROUNDS = 1

class Subsession(BaseSubsession):
    None


class Group(BaseGroup):
    None 

class Player(BasePlayer):
    age = models.IntegerField(
        min=18, max=99, 
        label= 'Wie alt sind Sie?' , 
    )
    gender = models.IntegerField(
    choices=[
        [1, 'Weiblich'],
        [2, 'Männlich'],
        [3, 'Divers'],
        [0, 'Keine Angabe'],
    ], 
    label= 'Welchem Geschlecht gehören Sie an?', 
    widget=widgets.RadioSelect
)
    semester = models.IntegerField(
        min=1, max=20, 
        label= 'In welchem Semester studieren Sie derzeit (einschließlich des Bachelorsemesters)?',
        blank = True,
        null = True  
)   
    studyfield = models.IntegerField(
        choices=[
        [0, 'Architektur'],
        [1, 'Bauingenieurwesen, Erd- und Umweltwissenschaften'],
        [2, 'Chemie und Biowissenschaften'],
        [3, 'Chemie- und Verfahrenstechnik'],
        [4, 'Elektrotechnik und Informationstechnik'],
        [5, 'Geistes- und Sozialwissenschaften'],
        [6, 'Computerwissenschaften'],
        [7, 'Maschinenwesen'],
        [8, 'Mathematik'],
        [9, 'Physik'],
        [10, 'Wirtschaftswissenschaften'],
        [11, 'Andere'],
    ], 
    label= 'In welcher Fakultät oder welchem Fachbereich studieren Sie?', 
    widget=widgets.RadioSelect
)
    KD2Lab = models.BooleanField(
        choices=[
        [True, 'Ja'],
        [False, 'Nein'],
    ], 
    widget=widgets.RadioSelect, 
    label= 'Haben Sie bereits an anderen Experimenten im KD²Lab teilgenommen (persönlich und/oder online)?' 
)
    Spieltheorie = models.BooleanField(
        choices=[
        [True, 'Ja'],
        [False, 'Nein'],
    ], 
    widget=widgets.RadioSelect, 
    label= 'Haben Sie bereits eine Vorlesung zur Spieltheorie besucht?' 
    )    
    Comments = models.StringField(
    blank=True, 
    null=True,
    label= 'Haben Sie Anmerkungen zu dem Experiment? (Bitte geben Sie hier keine personenbezogenen Informationen ein, die Aufschluss über Ihre Identität geben könnten)'
)
  
# FUNCTIONS    

# PAGES
class Quesionaire_two(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'semester', 'studyfield', 'KD2Lab', 'Spieltheorie', 'Comments' ]


page_sequence = [Quesionaire_two]


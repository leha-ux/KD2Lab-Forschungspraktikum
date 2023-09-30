from otree.api import *
import random

doc = """
prisonerTestgame
"""


class C(BaseConstants):
    NAME_IN_URL = 'TestSzenario1'
    PLAYERS_PER_GROUP = 2
    correct_answer = True

    # this is the number of supergames
    NUM_ROUNDS = 1
    STOPPING_PROBABILITY = 1

    PAYOFFA = cu(10)
    PAYOFFB = cu(5)
    PAYOFFC = cu(2)
    PAYOFFD = cu(0)

    # True is cooperate, False is defect
    PAYOFF_MATRIX = {
        (True, True): (PAYOFFB, PAYOFFB),
        (True, False): (PAYOFFD, PAYOFFA),
        (False, True): (PAYOFFA, PAYOFFD),
        (False, False): (PAYOFFC, PAYOFFC),
    }


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    iteration = models.IntegerField(initial=0)
    finished_sg = models.BooleanField(initial=False)


def live_method(player, data):
    group = player.group
    my_id = player.id_in_group
    
    if 'coop' in data:
        
        coop = data['coop']
        
        
        if coop == True:
            player.my_value = 0
        if coop == False:
            player.my_value = 1
            
    if group.finished_sg:
        return {my_id: dict(finished_sg=True)}

    [game] = Game.filter(group=group, iteration=group.iteration)
    
    coop_field = 'coop{}'.format(my_id)
    if 'coop' in data:
        
        coop = data['coop']
        
        print(coop)
        if coop == True:
            player.my_value = 0
        if coop == False:
            player.my_value = 1
            
        if getattr(game, coop_field) is not None:
            return
        setattr(game, coop_field, coop)
        
            
        coops = (game.coop1, game.coop2)
        #Auf True gesetzt, nicht auf Partner warten
        #is_ready = None not in coops
        is_ready = True
        if is_ready:
            #p1, p2 = group.get_players()
            #[game.payoff1, game.payoff2] = C.PAYOFF_MATRIX[coops]
            #Runde ist nicht relevant für echten Payout
            #p1.payoff += game.payoff1
            #p2.payoff += game.payoff2

            game.has_results = True
            group.iteration += 1
            
            # random stopping rule
            if random.random() < C.STOPPING_PROBABILITY:
                group.finished_sg = True
                group = player.group
                my_id = player.id_in_group
                return {my_id: dict(finished_sg=True)}

            Game.create(group=group, iteration=group.iteration)

            return {
                0: dict(should_wait=False, last_results=to_dict(game), iteration=group.iteration)
            }
    i_decided = getattr(game, coop_field) is not None
    if group.iteration > 0:
        [prev_game] = Game.filter(group=group, iteration=group.iteration - 1)
        last_results = to_dict(prev_game)
    else:
        last_results = None
    return {
        my_id: dict(
            should_wait=i_decided and not game.has_results,
            last_results=last_results,
            iteration=group.iteration,
        )
    }


class Game(ExtraModel):
    group = models.Link(Group)
    iteration = models.IntegerField()
    coop1 = models.CurrencyField()
    coop2 = models.CurrencyField()
    payoff1 = models.CurrencyField()
    payoff2 = models.CurrencyField()
    has_results = models.BooleanField(initial=False)


def to_dict(game: Game):
    pass 


class Player(BasePlayer):
    iteration = models.IntegerField(initial=0)
    my_value = models.IntegerField()
    comprehensioncheckNumber = models.BooleanField(
        choices=[
            [True, 'In Szenario1 entscheiden Sie zwischen zwei Optionen.'],
            [False, 'In Szenario1 hängt Ihr Ergebnis nicht von der Entscheidung des Mitspielers ab.'],
            [False, 'In Szenario1 entscheiden Sie, wie viel Geld zwei Mitspieler bekommen.'],
            [False, 'Alle vorhergenannten Antworten sind richtig']
        ],
        label='Welche der folgenden Aussagen ist richtig?',
        widget=widgets.RadioSelect
    )
    is_correct = models.BooleanField()

class WaitToStart(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        # make the first one
        Game.create(group=group, iteration=group.iteration)

class Anleitung(Page): 
    pass 

class Play(Page):
    form_model = 'player'
    live_method = live_method
    game_value = models.IntegerField()
    
    @staticmethod
    def js_vars(player: Player):
        return dict(my_id=player.id_in_group)


class Results(Page):
    pass

class Question(Page):
    form_model = 'player'
    form_fields = ['comprehensioncheckNumber']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.comprehensioncheckNumber == True:
            player.is_correct = True
            
        else:
            player.is_correct = False
            

class richtigeAntwort(Page):
    @staticmethod
    def is_displayed(player:Player): 
        return player.is_correct == True

    @staticmethod
    def vars_for_template(player: Player):
            return dict(
            is_correct=player.is_correct,
            correct_answer=C.correct_answer
            )
            
class falscheAntwort(Page): 
    @staticmethod
    def is_displayed(player:Player):
        # Überprüfen Sie die Bedingungen, ob die Seite übersprungen werden soll
        return player.is_correct == False  


page_sequence = [Anleitung, WaitToStart, Play, Results, Question, richtigeAntwort, falscheAntwort]

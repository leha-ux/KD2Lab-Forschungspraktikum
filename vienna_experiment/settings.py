from os import environ
OTREE_PRODUCTION = 1
DEBUG = False
SESSION_CONFIGS = [
    dict(
        name='vienna_experiment',
        display_name="Vienna Experiment",
        #app_sequence=['descendingPriceAuctionCond1'],

        
        
        
        #Full
        
        app_sequence=['startPage','Instruktionen',
                      'prisonerTestgame','descendingPriceAuctionTestgame', 
                      'prisonerCond1',
                      'prisonerCond2', 
                      'prisonerCond3',
                      'questionnaire_one','questionnaire_two','Payoff'],
        
        #app_sequence=['descendingPriceAuctionPupilCond3'],
        num_demo_participants=2,
    ),
]


# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)
OTREE_PRODUCTION=0
PARTICIPANT_FIELDS = [
    'is_dropout', 
    'treatment',
    'booking_time',
    'cards',
    'order',
    'reaction_times',
    'read_mind_in_eyes_score',
    'responses',
    'stimuli',
    'svo_angle',
    'svo_category',
]
SESSION_FIELDS = [
    'params',
    'finished_p1_list', 
    'iowa_costs', 
    'wisconsin', 
    'intergenerational_history'
    ]

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans

#If changed to anything else than 'en', the timer in descendingPriceAuction wont work anymore
LANGUAGE_CODE = 'de'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'EUR'
USE_POINTS = False

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '4544989454571'

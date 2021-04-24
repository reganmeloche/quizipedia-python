import os

class Config(object):
    DEBUG = False
    TESTING = False
    SCORE_OPTIONS = {
        'INITIAL_SCORE': os.environ.get('SCORE_OPTIONS.INITIAL_SCORE', default=10),
        'NON_WORD_PENALTY': os.environ.get('SCORE_OPTIONS.NON_WORD_PENALTY', default=3),
        'REPEAT_PENALTY': os.environ.get('SCORE_OPTIONS.REPEAT_PENALTY', default=3),
        'RANDOM_FACTOR': os.environ.get('SCORE_OPTIONS.RANDOM_FACTOR', default=2),
    }
    GAME_OPTIONS = {
        'SCORE_THRESHOLD': os.environ.get('GAME_OPTIONS.SCORE_THRESHOLD',default=13)
    }
    AUTH_OPTIONS = {
        'JWT_SECRET': 'my-secret',
        'API_USER': 'quizipedia-api'
    }
    TEST_CONFIG_VALUE = "my-default-value"

class ProductionConfig(Config):
    AUTH_OPTIONS = {
        'JWT_SECRET': os.environ.get('AUTH_OPTIONS.JWT_SECRET'),
        'API_USER': 'quizipedia-api'
    }
    TEST_CONFIG_VALUE = "my-prod-value"

class DevelopmentConfig(Config):
    TEST_CONFIG_VALUE = "my-dev-value"

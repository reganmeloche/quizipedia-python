from .GameOptions import GameOptions
from .ScoreOptions import ScoreOptions

class Options:
  def __init__(self, 
    game_options,
    score_options
  ):
    self.game_options = game_options
    self.score_options = score_options
  
  @staticmethod
  def from_config(config):
    game_config = config["GAME_OPTIONS"]
    game_options = GameOptions(
        game_config["SCORE_THRESHOLD"]
    )
    
    score_config = config["SCORE_OPTIONS"]
    score_options = ScoreOptions(
        score_config["INITIAL_SCORE"],
        score_config["NON_WORD_PENALTY"],
        score_config["REPEAT_PENALTY"],
        score_config["RANDOM_FACTOR"]
    )

    return Options(game_options, score_options)



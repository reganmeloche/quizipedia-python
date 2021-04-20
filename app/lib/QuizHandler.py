import copy

from .GameBuilder import GameBuilder
from .ScoreCalculator import ScoreCalculator

from ..classes.QuizResult import QuizResult


class QuizHandler:
  def __init__(self, nlp, word_set, default_options):
    self.nlp = nlp
    self.word_set = word_set
    self.default_options = default_options

  def handle(self, req_data):
    quiz_text = req_data['text']
    game_id = req_data['id']
    options = req_data.get('options')
    tokens = self.nlp(quiz_text)

    # TODO: Will want some sort of coalescing eventually. Maybe another static class?
    if options is None:
      options = copy.deepcopy(self.default_options)

    score_calculator = ScoreCalculator(options.score_options, self.word_set)

    built_game = GameBuilder(game_id, score_calculator, options.game_options, tokens)

    return QuizResult(
      game_id, 
      quiz_text, 
      built_game.game_array(), 
      built_game.relevant_words(), 
      built_game.analytics()
    )


from .QuizResult import QuizResult
import json
import copy
from spacy.matcher import Matcher
from .ScoreCalculator import ScoreCalculator
from .RelevantWord import RelevantWord
from .GameBit import GameBit
from .ScoreOptions import ScoreOptions

class QuizBuilderV2:
  score_threshold = 13

  def __init__(self, nlp, score_calculator):
    self.nlp = nlp
    self.score_calculator = score_calculator
    self.game_array = []
    self.word_list = []
    self.tracking_index = 0

  def build(self, req_data):
    quiz_text = req_data['text']
    game_id = req_data['id']
    self.doc = self.nlp(quiz_text)
    
    for token in self.doc:
      #print(token.i, token.text, token.pos_, token.pos, len(token))
      self.__handle_token(token, game_id)
    self.__load_span(len(self.doc))
  
    game_array = copy.deepcopy(self.game_array)
    relevant_words = copy.deepcopy(self.word_list)
    result = QuizResult(game_id, quiz_text, game_array, relevant_words)

    # Haven't figured out this part yet...
    result.analytics = None

    return result


  ################
  ### HANDLERS ###
  ################
  def __handle_new_line(self, token):
    self.__load_span(token.i)
    new_line_bit = GameBit('newLine', '')
    self.game_array.append(new_line_bit)

  def __handle_regular_word(self, token):
    # May not want to increase word distance on thigns like punct, etc
    if (token.pos != 97):
      self.score_calculator.add_word_distance()

  def __handle_relevant_word(self, game_id, token, score):
    self.score_calculator.reset_word_distance()
    new_word = RelevantWord(game_id, token.text, token.text, len(self.word_list))
    self.score_calculator.add_used_word(token.text)
    self.word_list.append(new_word)

    # load any previous text onto game array
    self.__load_span(token.i)
    
    # add the rword to the game array
    rword_bit = GameBit('rWord', token.text, new_word.index)
    self.game_array.append(rword_bit)


  ###############
  ### HELPERS ###
  ###############
  def __load_span(self, last_index):
    if (last_index > self.tracking_index):
      span = self.doc[self.tracking_index : last_index]
      next_game_bit = GameBit('text', span.text)
      self.game_array.append(next_game_bit)
      self.tracking_index = last_index + 1

  def __initial_check(self, token):
    return not token.is_stop and len(token.text) > 3

  def __is_new_line(self, token):
    return token.pos == 103 ## SPACE = new line


  ##############
  ### DRIVER ###
  ##############

  def __handle_token(self, token, game_id):
    if self.__is_new_line(token):
        self.__handle_new_line(token)
        return

    if self.__initial_check(token):
      score = self.score_calculator.calculate(token)

      if (score.total() > QuizBuilderV2.score_threshold):
        self.__handle_relevant_word(game_id, token, score)
        # Do something with the score and analytics...
        return
    
    self.__handle_regular_word(token)  


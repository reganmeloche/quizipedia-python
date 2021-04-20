import json
import copy

from ..classes.RelevantWord import RelevantWord
from ..classes.GameBit import GameBit
from ..classes.AnalyticsBit import AnalyticsBit

class GameBuilder:
  def __init__(self, game_id, score_calculator, game_options, tokens):
    # Private members
    self.__game_id = game_id
    self.__score_calculator = score_calculator
    self.__game_options = game_options
    self.__tracking_index = 0
    self.__tokens = tokens

    # Publically gettable (see getters)
    self.__game_array = []
    self.__relevant_words = []
    self.__analytics = { 'relevant_words': [] }
    
    for token in self.__tokens:
      #print(token.i, token.text, token.pos_, token.pos, len(token))
      self.__handle_token(token)
    self.__load_span(len(self.__tokens))


  ################
  ### GETTERS ####
  ################
  def relevant_words(self): return self.__relevant_words
  def game_array(self): return self.__game_array
  def analytics(self): return self.__analytics


  ################
  ### HANDLERS ###
  ################
  def __handle_new_line(self, token):
    self.__load_span(token.i)
    for i in range(token.text.count('\n')):
      new_line_bit = GameBit('newLine', '')
      self.__game_array.append(new_line_bit)

  def __handle_regular_word(self, token):
    # May not want to increase word distance on things like punct, etc
    if (token.pos != 97):
      self.__score_calculator.add_word_distance()

  def __handle_relevant_word(self, game_id, token, score):
    self.__score_calculator.reset_word_distance()
    new_word = RelevantWord(game_id, token.text, token.text, len(self.__relevant_words))
    self.__score_calculator.add_used_word(token.text)
    self.__relevant_words.append(new_word)

    # load any previous text onto game array
    self.__load_span(token.i)
    
    # add the rword to the game array
    rword_bit = GameBit('rWord', token.text, new_word.index)
    self.__game_array.append(rword_bit)


  ###############
  ### HELPERS ###
  ###############
  def __load_span(self, last_index):
    if (last_index > self.__tracking_index):
      span = self.__tokens[self.__tracking_index : last_index]
      next_game_bit = GameBit('text', span.text)
      self.__game_array.append(next_game_bit)
      self.__tracking_index = last_index + 1

  def __passes_initial_check(self, token):
    return not token.is_stop and len(token.text) > 3

  def __is_new_line(self, token):
    return token.pos == 103 ## SPACE = new line


  ##############
  ### DRIVER ###
  ##############

  def __handle_token(self, token):
    if self.__is_new_line(token):
        self.__handle_new_line(token)
        return

    if self.__passes_initial_check(token):
      score = self.__score_calculator.calculate(token)

      if (score.total() > self.__game_options.score_threshold):
        self.__handle_relevant_word(self.__game_id, token, score)
        self.__analytics['relevant_words'].append(AnalyticsBit(token.text, score))
        return
    
    self.__handle_regular_word(token)  

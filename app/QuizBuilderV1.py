from .QuizResult import QuizResult
import json
import random
import copy
from spacy.matcher import Matcher
from .WordScore import WordScore
from .RelevantWord import RelevantWord
from .GameBit import GameBit


class QuizBuilderV1:
  initial_score = 10
  non_word_penalty = 3
  score_threshold = 10

  def __init__(self, nlp):
    self.nlp = nlp
    self.game_array = []
    self.word_list = []
    self.curr_text_array = []
    self.word_distance = 0
    self.used_words = []
    self.random_factor = 2

  def build(self, req_data):
    quiz_text = req_data['text']
    game_id = req_data['id']
    doc = self.nlp(quiz_text)
    self.word_list = []
    self.game_array = []
    
    for token in doc:
      #(token.text, token.pos_, token.pos)
      self.__handle_token(token, game_id)   
  
    game_array = copy.deepcopy(self.game_array)
    relevant_words = copy.deepcopy(self.word_list)
    result = QuizResult(game_id, quiz_text, game_array, relevant_words)

    result.analytics = None

    return result

  def __handle_regular_word(self, token):
    self.word_distance += 1
    self.curr_text_array.append(token.text)

  def __handle_relevant_word(self, game_id, token, score):
    self.word_distance = 0
    new_word = RelevantWord(game_id, token.text, token.text, len(self.word_list))
    self.used_words.append(token.text)
    self.word_list.append(new_word)

    # load any previous text onto game array
    self.__load_game_array('text')
    
    # add the rword to the game array
    rword_bit = GameBit('rWord', token.text, new_word.index)
    self.game_array.append(rword_bit)


  # separate public function. Will need to control the members...
  def __calculate_score(self, token):
    score = WordScore()

    score.length_score = QuizBuilderV1.initial_score - max(0, len(token) - 10)

    # use something else - this doesnt work
    if (token.text not in self.nlp.vocab):
      score.real_word_score = -QuizBuilderV1.non_word_penalty
    
    for x in [x for x in self.used_words if x == token.text]:
      score.repeat_score -= 3

    score.distance_score += self.word_distance

    score.random_score += random.randint(0, self.random_factor*2) - self.random_factor
    
    return score


  def __initial_check(self, token):
    return not token.is_stop and len(token.text) > 3

  def __handle_new_line(self):
    self.__load_game_array('text')
    new_line_bit = GameBit('newLine', '')
    self.game_array.append(new_line_bit)

  def __is_new_line(self, token):
    return token.pos == 103 ## SPACE = new line

  def __load_game_array(self, bit_type):
    if (len(self.curr_text_array) > 0):
      value = (' ').join(self.curr_text_array)
      next_game_bit = GameBit(bit_type, value)
      self.game_array.append(next_game_bit)
      self.curr_text_array = []

  def __handle_token(self, token, game_id):
    if self.__is_new_line(token):
        self.__handle_new_line()
        return

    if self.__initial_check(token):
      score = self.__calculate_score(token)

      if (score.total() > QuizBuilderV1.score_threshold):
        self.__handle_relevant_word(game_id, token, score)
        # Do something with the score and analytics...
        return
    
    self.__handle_regular_word(token)  
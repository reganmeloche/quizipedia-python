from .WordScore import WordScore
import random

class ScoreCalculator:
  def __init__(self, options, word_set):
    self.__word_distance = 0
    self.__used_words = []
    self.__word_set = word_set

    # Options
    self.__random_factor = options.random_factor 
    self.__initial_score = options.initial_score
    self.__non_word_penalty = options.non_word_penalty
    self.__repeat_penalty = options.repeat_penalty
    # likely need nlp and doc access...

  def add_word_distance(self):
    self.__word_distance += 1
  
  def reset_word_distance(self):
    self.__word_distance = 0
  
  def add_used_word(self, word):
    self.__used_words.append(word)

  ## Add some descriptions here
  def calculate(self, token):
    score = WordScore()
    #print(token, token.pos, token.pos_, token.ent_type, token.ent_type_)

    score.length_score = self.__initial_score - max(0, len(token) - 10)

    if token.lemma_.lower() not in self.__word_set:
      score.real_word_score -= self.__non_word_penalty
    
    for x in [x for x in self.__used_words if x == token.text]:
      score.repeat_score -= self.__repeat_penalty

    score.word_type_score += self._get_word_type_score(token)
    
    # Could add something for entity type recognition (token.ent_type_)...

    score.distance_score += self.__word_distance

    score.random_score += random.randint(0, self.__random_factor*2) - self.__random_factor

    return score

  def _get_word_type_score(self, token):

    noun = 92
    #propn = 96
    verb = 100
    adj = 84
    num = 93
    adv = 86
    minus_list = [num, adv, verb]
    plus_list = [noun, adj]
    result = 0

    pos = token.pos
    if pos in minus_list:
      result = -1
    elif pos in plus_list:
      result = +1
    
    return result
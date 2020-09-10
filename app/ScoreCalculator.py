from .WordScore import WordScore
import random
import enchant

class ScoreCalculator:
  def __init__(self, options):
    self.__word_distance = 0
    self.__used_words = []
    self.__word_checker = enchant.Dict("en_US") # inject/interface...

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

    score.length_score = self.__initial_score - max(0, len(token) - 10)

    if not self.__word_checker.check(token.text):
      score.real_word_score -= self.__non_word_penalty
    
    for x in [x for x in self.__used_words if x == token.text]:
      score.repeat_score -= self.__repeat_penalty

    # Want something to measure the relevance with spacy...

    score.distance_score += self.__word_distance

    score.random_score += random.randint(0, self.__random_factor*2) - self.__random_factor

    return score

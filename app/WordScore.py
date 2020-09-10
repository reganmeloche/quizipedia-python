class WordScore:
  def __init__(self):
    self.length_score = 0
    self.real_word_score = 0
    self.distance_score = 0
    self.random_score = 0
    self.repeat_score = 0

  def total(self):
    return self.length_score + self.real_word_score + self.distance_score + self.random_score + self.repeat_score

  def print_me(self):
    print('-- length', self.length_score)
    print('-- real word', self.real_word_score)
    print('-- distance', self.distance_score)
    print('-- random', self.random_score)
    print('-- repeat', self.repeat_score)
    print('-- TOTAL', self.total())

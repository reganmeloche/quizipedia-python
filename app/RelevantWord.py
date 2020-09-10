class RelevantWord:
  def __init__(self, game_id, word, stripped_word, index):
    self.game_id = game_id
    self.answer = word
    self.stripped_word = stripped_word
    self.index = index
    self.hints = 0
    self.points = max(5, len(word) - 4)
    self.blank = '_' * len(word)
    self.possible_answers = [word]
  


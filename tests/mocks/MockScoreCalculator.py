from app.WordScore import WordScore

class MockScoreCalculator:
  #def __init__(self):

  def add_word_distance(self):
    return
  
  def reset_word_distance(self):
    return
  
  def add_used_word(self, word):
    return

  def calculate(self, token):
    pass_words = ['test', 'interesting', 'coffee', 'mystery']
    score = WordScore()
    if (token.text in pass_words):
        score.distance_score = 20
    return score


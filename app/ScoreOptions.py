class ScoreOptions:
  def __init__(self, 
    initial_score,
    non_word_penalty,
    repeat_penalty,
    random_factor
  ):
    self.initial_score = initial_score
    self.non_word_penalty = non_word_penalty
    self.repeat_penalty = repeat_penalty
    self.random_factor = random_factor

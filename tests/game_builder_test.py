import unittest

from app.lib.GameBuilder import GameBuilder
from app.nlp.nlp_init import init_nlp
from app.options.GameOptions import GameOptions

from .mocks.MockScoreCalculator import MockScoreCalculator

class GameBuilderTests(unittest.TestCase):
    def setUp(self):
        self.nlp = init_nlp()
        
        # Should maybe pass in the pass_words into the constructor...
        self.score_calculator = MockScoreCalculator()
    
    def test_quiz_building(self):
        test_text = 'This is a test...\nHere is a new interesting line which has the following types of coffee: arabica, robusta, and the so-called "mystery flavour"!!'
        tokens = self.nlp(test_text)
        game_options = GameOptions(13)
        result = GameBuilder('abcd1234', self.score_calculator, game_options, tokens)
        
        game_array = result.game_array()

        self.assertEqual(len(result.relevant_words()), 4)


        ga0 = game_array[0]
        self.assertEqual(ga0.type, 'text')
        self.assertEqual(ga0.value, 'This is a')

        ga1 = game_array[1]
        self.assertEqual(ga1.type, 'rWord')
        self.assertEqual(ga1.value, 'test')
        self.assertEqual(ga1.index, 0)

        ga2 = game_array[2]
        self.assertEqual(ga2.type, 'text')
        self.assertEqual(ga2.value, '...')

        ga3 = game_array[3]
        self.assertEqual(ga3.type, 'newLine')
        self.assertEqual(ga3.value, '')


if __name__ == '__main__':
    unittest.main()
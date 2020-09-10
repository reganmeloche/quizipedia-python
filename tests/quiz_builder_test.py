import unittest
import json
from app.ScoreCalculator import ScoreCalculator
from app.QuizBuilderV2 import QuizBuilderV2
import spacy
from app.commonWords import common_words
from app.ScoreOptions import ScoreOptions
from .mocks.MockScoreCalculator import MockScoreCalculator

class TestQuizBuilder(unittest.TestCase):
    def setUp(self):
        # nlp should come from a func - reuse
        nlp = spacy.load('en_core_web_sm')
        nlp.Defaults.stop_words |= common_words

        # Should maybe pass in the pass_words into the constructor...
        score_calculator = MockScoreCalculator()
        self.sut = QuizBuilderV2(nlp, score_calculator)
    
    def test_quiz_building(self):
        data = {
            'id': 'abcd1234',
            'text': 'This is a test...\nHere is a new interesting line which has the following types of coffee: arabica, robusta, and the so-called "mystery flavour"!!'
        }
        
        result = self.sut.build(data)

        self.assertEqual(len(result.relevant_words), 4)

        ga0 = result.game_array[0]
        self.assertEqual(ga0.type, 'text')
        self.assertEqual(ga0.value, 'This is a')

        ga1 = result.game_array[1]
        self.assertEqual(ga1.type, 'rWord')
        self.assertEqual(ga1.value, 'test')
        self.assertEqual(ga1.index, 0)

        ga2 = result.game_array[2]
        self.assertEqual(ga2.type, 'text')
        self.assertEqual(ga2.value, '...')

        ga3 = result.game_array[3]
        self.assertEqual(ga3.type, 'newLine')
        self.assertEqual(ga3.value, '')



if __name__ == '__main__':
    unittest.main()
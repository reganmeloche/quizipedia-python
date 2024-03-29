import unittest

from app.lib.ScoreCalculator import ScoreCalculator
from app.nlp.nlp_init import init_nlp, init_words
from app.options.ScoreOptions import ScoreOptions

class ScoreCalculateTests(unittest.TestCase):
    def setUp(self):
        nlp = init_nlp()
        word_set = init_words()

        self.mock_doc = nlp('Test alpha xyzhungeepgy jupiter anthropomorphic')
        options = ScoreOptions(10, 3, 3, 0)
        self.sut = ScoreCalculator(options, word_set)
    
    def test_0(self):
        result = self.sut.calculate(self.mock_doc[0])
        self.assertEqual(result.length_score, 10)
        self.assertEqual(result.random_score, 0)
        self.assertEqual(result.real_word_score, 0)
        self.assertEqual(result.repeat_score, 0)
        self.assertEqual(result.distance_score, 0)
        self.assertEqual(result.word_type_score, 0)
        self.assertEqual(result.total(), 10)
    
    def test_1(self):
        self.sut.add_word_distance()
        self.sut.add_used_word('alpha')
        result = self.sut.calculate(self.mock_doc[1])
        self.assertEqual(result.length_score, 10)
        self.assertEqual(result.random_score, 0)
        self.assertEqual(result.real_word_score, 0)
        self.assertEqual(result.repeat_score, -3)
        self.assertEqual(result.distance_score, 1)
        self.assertEqual(result.word_type_score, 1)
        self.assertEqual(result.total(), 9)

    def test_2(self):
        result = self.sut.calculate(self.mock_doc[2])
        self.assertEqual(result.length_score, 8)
        self.assertEqual(result.random_score, 0)
        self.assertEqual(result.real_word_score, -3)
        self.assertEqual(result.repeat_score, 0)
        self.assertEqual(result.distance_score, 0)
        self.assertEqual(result.word_type_score, 0)
        self.assertEqual(result.total(), 5)

if __name__ == '__main__':
    unittest.main()
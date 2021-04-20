import spacy
import nltk
nltk.download('words')
from nltk.corpus import words
from .commonWords import common_words

def init_nlp():
    nlp = spacy.load('en_core_web_sm')
    nlp.Defaults.stop_words |= common_words
    return nlp

def init_words():
    word_set = set(words.words())
    return word_set


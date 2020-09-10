from flask import Flask, request, Response, jsonify
import json
import jsonpickle
import spacy
import nltk
nltk.download('words')
from nltk.corpus import words

from .parser import Parser
from .QuizBuilderV2 import QuizBuilderV2
from .QuizBuilderV1 import QuizBuilderV1
from .ScoreCalculator import ScoreCalculator
from .ScoreOptions import ScoreOptions
from .commonWords import common_words

app = Flask(__name__) 

with app.app_context():
    # Eventually have a separate file for nlp setup
    nlp = spacy.load('en_core_web_sm')
    nlp.Defaults.stop_words |= common_words
    word_set = set(words.words())
    
    @app.route("/") 
    def home_view(): 
            return "<h1>Welcome!</h1>"

    @app.route('/tester', methods=['POST'])
    def tester():
        p1 = Parser('MyParser')
        req_data = request.get_json()
        result = p1.parse(req_data)
        return result

    @app.route('/v2/quiz', methods=['POST'])
    def quiz():
        builder = QuizBuilderV2(nlp, _get_score_calculator())
        req_data = request.get_json() # deserialize into object?
        quiz_result = builder.build(req_data)
        json_response = jsonpickle.encode(quiz_result)
        return Response(json_response, mimetype='application/json')

    @app.route('/v1/quiz', methods=['POST'])
    def quizLegacy():
        builder = QuizBuilderV1(nlp)
        req_data = request.get_json()
        quiz_result = builder.build(req_data)
        json_response = jsonpickle.encode(quiz_result)
        return Response(json_response, mimetype='application/json')
    

    ###############
    ### HELPERS ###
    ###############

    def _get_score_calculator():
        score_options = ScoreOptions(10, 3, 3, 2) # get from config
        return ScoreCalculator(score_options, word_set)

from flask import Flask, request, Response, jsonify
import json
import jsonpickle
import os

from .lib.QuizHandler import QuizHandler
from .options.Options import Options
from .nlp.nlp_init import init_nlp, init_words
from .config import ProductionConfig, DevelopmentConfig

app = Flask(__name__) 

print(os.environ.get("FLASK_ENV"))
print(app.env)
print(app.config["ENV"])

if (app.env == 'production'):
    app.config.from_object(ProductionConfig)
else:
    app.config.from_object(DevelopmentConfig)

print(app.config["JWT_SECRET"])
print(app.config["TEST_CONFIG_VALUE"])
print(app.config["GAME_OPTIONS"])

with app.app_context():
    # Init and Dependency Injection
    nlp = init_nlp()
    word_set = init_words()
    default_options = Options.from_config(app.config)
    quiz_handler = QuizHandler(nlp, word_set, default_options)
    
    @app.route("/") 
    def home_view(): 
            return "Hello!"

    @app.route('/v2/quiz', methods=['POST'])
    def quiz():
        req_data = request.get_json()
        quiz_result = quiz_handler.handle(req_data)
        json_response = jsonpickle.encode(quiz_result)
        return Response(json_response, mimetype='application/json')

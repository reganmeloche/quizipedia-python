from flask import Flask, request, Response, jsonify
import json
import jsonpickle
import os

from .auth_lib import AuthLib
from .lib.QuizHandler import QuizHandler
from .options.Options import Options
from .nlp.nlp_init import init_nlp, init_words
from .config import ProductionConfig, DevelopmentConfig
from .helpers.exceptions import AuthError

app = Flask(__name__) 

if (app.env == 'production'):
    app.config.from_object(ProductionConfig)
else:
    app.config.from_object(DevelopmentConfig)

with app.app_context():
    # Init and Dependency Injection
    nlp = init_nlp()
    word_set = init_words()
    default_options = Options.from_config(app.config)
    quiz_handler = QuizHandler(nlp, word_set, default_options)
    auth_lib = AuthLib(default_options.auth_options)
    
    @app.route("/") 
    @auth_lib.requires_auth
    def home_view(): 
            return "Hello!"
    
    @app.route('/token')
    def generate():
        if (app.env == 'production'):
            return 'get outta heeeeere!'
        else:
            return auth_lib.generate_token()

    @app.route('/v2/quiz', methods=['POST'])
    @auth_lib.requires_auth
    def quiz():
        req_data = request.get_json()
        quiz_result = quiz_handler.handle(req_data)
        json_response = jsonpickle.encode(quiz_result)
        return Response(json_response, mimetype='application/json')
    
    @app.errorhandler(AuthError)          
    def handle_auth(e):          
        return "Auth Error: " + str(e.error), e.status_code

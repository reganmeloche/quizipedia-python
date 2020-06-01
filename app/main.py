from flask import Flask, request
from .parser import Parser

app = Flask(__name__) 
  
@app.route("/") 
def home_view(): 
        return "<h1>Welcome!</h1>"

@app.route('/tester', methods=['POST'])
def tester():
    p1 = Parser('MyParser')
    req_data = request.get_json()
    result = p1.parse(req_data)
    return result

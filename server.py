# import prerun
from flask import Flask, render_template, request
import json
from utils.summarizer import getSummary

app = Flask(__name__)

# @app.before_first_request
# def activate_job():
#     def run_job():    
#         os.system("bash setup.sh")
#         print(os.system("ls ./utils/saved_model/"))
#         print("server ready for requests")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/summary', methods = ['POST', 'GET'])
def summaryAPI():
    if request.method == 'POST':
        request_data = request.data.decode("utf-8")
        request_json = json.loads(request_data)
        print(request_json["text"])
        print(type(request_json["text"]))
        summary = getSummary(request_json["text"])
        return json.dumps({ "summary": summary });

def main():
    app.run()
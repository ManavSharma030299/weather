from flask import Flask, jsonify, request
from flask_ngrok import run_with_ngrok

app = Flask(__name__)
run_with_ngrok(app)  

@app.route('/')
def student_number():
    student_number = "200536293" 
    return jsonify({"student_number": student_number})

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True)
    if not req:
        return jsonify({"fulfillmentText": "Error: Invalid request"}), 400
    
    fulfillment_text = "Dynamic response from the webhook!"
    
    return jsonify({"fulfillmentText": fulfillment_text})

if __name__ == '__main__':
    app.run()
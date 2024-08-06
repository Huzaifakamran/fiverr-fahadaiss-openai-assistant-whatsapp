from flask import Flask, request
from dotenv import load_dotenv, find_dotenv
import json
import os
from openai_assistant import initialize_thread,create_message,bot_response
from twilio_functions import send_message

load_dotenv(find_dotenv())

# Path to your JSON file
json_file_path = 'details.json'

def load_json_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    return {}

def save_json_data(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)



app = Flask(__name__)

@app.route('/')
def home():
    return 'Go to /twilio/receiveMessage route'

@app.route('/twilio/receiveMessage', methods=['POST'])
def receiveMessage():
    try:
        message = request.form['Body']
        print('message',message)
        data = load_json_data(json_file_path)
        sender_id = request.form['From']
        print('senderid',sender_id)
        
        thread_id = None
        for thread in data.get('threads', []):
            if thread.get('sender_id') == sender_id:
                thread_id = thread.get('thread_id')
                break
        
        if thread_id is None:
            thread_id = initialize_thread()
            if 'threads' not in data:
                data['threads'] = []
            data['threads'].append({'thread_id': thread_id, 'sender_id': sender_id})
            save_json_data(json_file_path, data)
        print('thread_id',thread_id) 
        create_message(message, thread_id)
        response = bot_response(thread_id)
        print(response)
        send_message(sender_id, response)
    except Exception as e:
        print(f"Error: {e}")
        pass
    return 'OK', 200

if __name__ == '__main__':
    app.run(debug=True)
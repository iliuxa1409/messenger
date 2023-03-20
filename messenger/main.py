from flask import Flask, render_template, request
import json
from datetime import datetime


# upload messages from file
def load_message():
    with open('db.json', 'r') as json_file:
        data = json.load(json_file)
    return data['messages']


# add new messages
def add_message(sender, text):
    new_message = {
        'text': text,
        'sender': sender,
        'time': datetime.now().strftime('%H:%M')
    }
    all_messages.append(new_message)


# def save file
def save_messages():
    data = {
        'messages': all_messages
    }
    with open('db.json', 'w') as json_file:  # w - write
        json.dump(data, json_file)


all_messages = load_message()

app = Flask(__name__)  # create new app


@app.route('/index')
def index_page():
    return 'Hello world!'


@app.route('/chat')
def display_chat():
    return render_template('form.html')


@app.route('/get_messages')
def get_messages():
    return {'messages': all_messages}


@app.route('/send_message')
def send_message():
    sender = request.args['name']
    text = request.args['text']
    add_message(sender, text)
    save_messages()
    return 'ok'


@app.route('/status')
def messages_users_number():
    users = []
    messages_num = 0
    for i in all_messages:
        if i['sender'] not in users:
            users.append(i['sender'])
        messages_num += 1

    return f'USERS: {str(len(users))} ' \
           f'\nMESSAGES: {str(messages_num)}'


app.run(host='0.0.0.0', port=80)  # server launch

from flask import Flask, render_template, request, redirect, url_for, jsonify, g
import json
from functools import wraps
import mysql.connector
import os
from werkzeug.utils import secure_filename
import ast
from flask import session
import requests
import ast
from transformers import pipeline
from datetime import datetime

qa_pipeline = pipeline("text2text-generation", model="google/flan-t5-large")





app = Flask(__name__)

def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(
            user='root',
            host='localhost',
            password='8307802643',
            database='gov',
            charset="utf8",
            port="3306",
        )
    return g.db



def execute_query(query, data=None):
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(query, data)
        db.commit()


def fetch_data(query, data=None, one=False):
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(query, data)
        if one:
            return cursor.fetchone()
        return cursor.fetchall()
    
def fetch_daata(query, data=None, one=False):
    db = get_dbb()
    with db.cursor() as cursor:
        cursor.execute(query, data)
        if one:
            return cursor.fetchone()
        return cursor.fetchall()
    

def get_dbb():
        db = mysql.connector.connect(
            user='root',
            host='localhost',
            password='8307802643',
            database='gov',
            charset="utf8",
            port="3306",
        )
        return db
    

cmd = "select * from scheme where title='WIDOW EMPOWERMENT YOJNA' "
daaata = fetch_daata(cmd)
data = daaata[0]
title = data[0]
objective = data[1]
descrip = data[2]
eligibility = data[3]
note = data[4]
state = data[5]
docs = data[6]


payload = f"Governement of India Have launched new scheme named {title} with an aim of {objective}. It is described as {descrip} with a special note that {note}. Eligibility criteria for this scheme is {eligibility} and for state {state} with documents required like {docs} "






@app.route('/')
def main():
    
    cmd="select title, objective from scheme "
    data = fetch_data(cmd)
    return render_template('index.html',data=data)




@app.route('/chat')
def chat():
    
  
    return render_template('chat.html')


@app.route('/generate', methods=['POST','GET'])
def generate_text():
    data = request.get_json()
    input_text = data.get('input_text', '')
    prompt = f"Paragraph: {payload}\n\nQuestion: {input_text}\n\nAnswer in 2-3 lines and if not sure much then say I am sorry cant help you with this:"

    # Use the model to generate the answer
    result = qa_pipeline(prompt, max_length=100, num_return_sequences=1)

    # Extract and print the answer from the result
    output = result[0]['generated_text']
    print(f"Answer: {output}")
    return jsonify(output)












if __name__ == '__main__':
    app.run(debug=True,port=7500)
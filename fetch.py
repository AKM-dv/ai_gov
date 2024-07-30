from transformers import pipeline
import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, jsonify, g
import json
from functools import wraps
import os
from werkzeug.utils import secure_filename
from flask import session
import requests
from datetime import datetime

def get_db():
    db = mysql.connector.connect(
        user='root',
        host='localhost',
        password='8307802643',
        database='gov',
        charset="utf8",
        port="3306",
    )
    return db

def fetch_data(query, data=None, one=False):
    db1 = get_db()
    with db1.cursor() as cursor:
        cursor.execute(query, data)
        if one:
            return cursor.fetchone()
        return cursor.fetchall()

# Load the model
qa_pipeline = pipeline("text2text-generation", model="google/flan-t5-large")

def split_text(text, max_tokens=512):
    words = text.split()
    for i in range(0, len(words), max_tokens):
        yield ' '.join(words[i:i + max_tokens])

def process_chunks(chunks, question):
    answers = []
    for chunk in chunks:
        prompt = f"Paragraph: {chunk}\n\nQuestion: {question}\n\nAnswer in 2-3 lines and if required 4-5 lines:"
        result = qa_pipeline(prompt, max_length=100, num_return_sequences=1)
        answers.append(result[0]['generated_text'])
    return " ".join(answers)

cmd = "select * from scheme"
daaata = fetch_data(cmd)
finalpayload = ""

for d in daaata:
    title = d[0]
    objective = d[1]
    descrip = d[2]
    eligibility = d[3]
    note = d[4]
    state = d[5]
    docs = d[6]
    payload = f"Governement of India Have launched new scheme named {title} with an aim of {objective}. It is described as {descrip} with a special note that {note}. Eligibility criteria for this scheme is {eligibility} and for state {state} with documents required like {docs} "
    finalpayload = finalpayload + "and another scheme is as follows" + payload

print(finalpayload)

while True:
    user_input = input("Enter your Question: ")
    chunks = list(split_text(finalpayload))
    answer = process_chunks(chunks, user_input)
    print(answer)

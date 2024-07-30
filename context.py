from transformers import pipeline
import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, jsonify, g



# Load the pre-trained model for text generation
qa_pipeline = pipeline("text2text-generation", model="google/flan-t5-large")


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




def execute_query(query, data=None):
    db1 = get_db()
    with db1.cursor() as cursor:
        cursor.execute(query, data)
        db1.commit()


def fetch_data(query, data=None, one=False):
    db1 = get_db()
    with db1.cursor() as cursor:
        cursor.execute(query, data)
        if one:
            return cursor.fetchone()
        return cursor.fetchall()


cmd = "select * from scheme where title='WIDOW EMPOWERMENT YOJNA' "
daaata = fetch_data(cmd)
data = daaata[0]
title = data[0]
objective = data[1]
descrip = data[2]
eligibility = data[3]
note = data[4]
state = data[5]
docs = data[6]


payload = f"Governement of India Have launched new scheme named {title} with an aim of {objective}. It is described as {descrip} with a special note that {note}. Eligibility criteria for this scheme is {eligibility} and for state {state} with documents required like {docs} "


while True:

    question = input("Enter your question: ")

    # Create the prompt by combining the paragraph and the question
    prompt = f"Paragraph: {payload}\n\nQuestion: {question}\n\nAnswer in 2-3 lines:"

    # Use the model to generate the answer
    result = qa_pipeline(prompt, max_length=100, num_return_sequences=1)

    # Extract and print the answer from the result
    answer = result[0]['generated_text']
    print(f"Answer: {answer}")

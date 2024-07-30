from transformers import pipeline
import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, jsonify, g




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
intents = ["information get", "apply for scheme", "file a grievance report"]

qa_pipeline = pipeline("text2text-generation", model="google/flan-t5-large")

# Function to classify intent
def classify_intent(user_input):
    # Use a prompt template to help the model classify the intent
    prompt = f"Classify the intent of the following input into one of these categories: {intents}.\n\nInput: {user_input}\n\nIntent:"

    # Generate the response
    response = qa_pipeline(prompt, max_length=10, num_return_sequences=1)[0]['generated_text']

    # Extract the classified intent
    classified_intent = response.split()[-1]

    return classified_intent



cmd = "select * from scheme  "
daaata = fetch_data(cmd)
finalpayload = ""

for i in daaata :

    data = daaata[0]
    title = data[0]
    objective = data[1]
    descrip = data[2]
    eligibility = data[3]
    note = data[4]
    state = data[5]
    docs = data[6]


    payload = f"Governement of India Have launched new scheme named {title} with an aim of {objective}. It is described as {descrip} with a special note that {note}. Eligibility criteria for this scheme is {eligibility} and for state {state} with documents required like {docs} "

    finalpayload = finalpayload + payload


def getdata(user_input):
    prompt = f"Paragraph: {finalpayload}\n\nQuestion: {user_input}\n\nAnswer in 2-3 lines:"

    # Use the model to generate the answer
    result = qa_pipeline(prompt, max_length=100, num_return_sequences=1)

    # Extract and print the answer from the result
    answer = result[0]['generated_text']
   
    return answer

def applyscheme(user_input):
    print("user_input")

def report(user_input):
    print("user_input")


# Example user input
while True :
        
    user_input = input("Enter your Question: ")
    intent = classify_intent(user_input)
    print(f"Classified Intent: {intent}")
    if intent=='get':
       result =  getdata(user_input)
       print(result)
    elif intent=="scheme":
        applyscheme(user_input)
    elif intent == "report":
        report(user_input)
    else:
        continue



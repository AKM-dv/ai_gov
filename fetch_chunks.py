from transformers import pipeline
import mysql.connector
import concurrent.futures
import hashlib

# Load the model
qa_pipeline = pipeline("text2text-generation", model="google/flan-t5-large")

# Database connection
def get_db():
    return mysql.connector.connect(
        user='root',
        host='localhost',
        password='8307802643',
        database='gov',
        charset="utf8",
        port="3306",
    )

def fetch_data(query):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return result

def split_text(text, max_tokens=512):
    words = text.split()
    for i in range(0, len(words), max_tokens):
        yield ' '.join(words[i:i + max_tokens])

def process_chunk(chunk, question):
    prompt = f"Paragraph: {chunk}\n\nQuestion: {question}\n\nAnswer in 2-3 lines and if required 4-5 lines:"
    result = qa_pipeline(prompt, max_length=100, num_return_sequences=1)
    return result[0]['generated_text']

def process_chunks(chunks, question):
    answers = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_chunk = {executor.submit(process_chunk, chunk, question): chunk for chunk in chunks}
        for future in concurrent.futures.as_completed(future_to_chunk):
            answers.append(future.result())
    return " ".join(answers)

# Simple cache implementation
cache = {}

def get_cached_response(query, question):
    query_hash = hashlib.md5((query + question).encode()).hexdigest()
    if query_hash in cache:
        return cache[query_hash]
    data = fetch_data(query)
    final_payload = ""
    for d in data:
        title, objective, descrip, eligibility, note, state, docs = d
        payload = (f"Governement of India Have launched new scheme named {title} with an aim of {objective}. "
                   f"It is described as {descrip} with a special note that {note}. Eligibility criteria for this "
                   f"scheme is {eligibility} and for state {state} with documents required like {docs}")
        final_payload += "and another scheme is as follows " + payload
    
    chunks = list(split_text(final_payload))
    answer = process_chunks(chunks, question)
    cache[query_hash] = answer
    return answer

if __name__ == '__main__':
    query = "SELECT * FROM scheme"
    while True:
        user_input = input("Enter your question: ")
        if user_input.lower() in ['exit', 'quit']:
            break
        answer = get_cached_response(query, user_input)
        print("Answer:", answer)

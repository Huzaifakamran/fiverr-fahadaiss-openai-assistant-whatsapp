from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

assistant_id = os.getenv("ASSISTANT_ID")

def initialize_thread():
    thread = client.beta.threads.create()
    return thread.id

def create_message(query, thread_id):
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=query
    )

def bot_response(thread_id):
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
    )
    while True:
        print('True')
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )
        
        if run.status == "completed":
            messages = client.beta.threads.messages.list(thread_id=thread_id)
            latest_message = messages.data[0]
            text = latest_message.content[0].text.value
            break
        elif run.status == "failed":
            return run.last_error.message
    return text
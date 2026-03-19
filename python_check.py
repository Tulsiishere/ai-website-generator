# check_models.py
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
client = genai.Client(api_key=os.getenv("AIzaSyDI9hybJ9SQ5R6dqHAOHuHB2zh1zDs8iPs"))

for model in client.models.list():
    print(model.name)
import os
import openai
import requests
from datetime import datetime
from tqdm import tqdm

openai.api_key = os.getenv("OPENAI_API_KEY")

models = openai.Model.list()
l = [x['id'] for x in models['data']]

print(l)

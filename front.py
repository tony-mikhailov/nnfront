import os
import io
import openai
import streamlit as st
import requests
from datetime import datetime
from PIL import Image
import time

root_dir = 'NN'

def get_models():
  models = openai.Model.list()
  return [x['id'] for x in models['data']]

def get_model_index(model_name):
  for i, x in enumerate(get_models()):
    if x == model_name:
      return i 

openai.api_key = os.getenv("OPENAI_API_KEY")

model = st.selectbox("NNModel", get_models(), index=get_model_index('gpt-3.5-turbo'))

img_count = st.slider('Images count', min_value=1, max_value=5)
temperature = st.slider('Temperature', min_value=0.0, max_value=1.0, step=0.01)

st.text_input("System", key="system_query")
st.text_input("Query", key="query")

op = st.selectbox("Whaht to do?", ['Chat', 'Img generation'])

# if not( "query" in st.session_state):
#   st.session_state.query = ''

if op == 'Chat':

  st.write("Process request: ", st.session_state.query)

  if st.session_state.query == '':
    exit()
  
  start_time = time.time()
  response = openai.ChatCompletion.create(
    model=model,
    messages=[
        {'role': 'system', 'content': st.session_state.system_query},
        {'role': 'user', 'content': st.session_state.query}
    ],
    temperature=temperature,
  )
  
  filename = f'{root_dir}/{datetime.now().strftime("%Y%m%dT%H%M%S")}_{model}.txt'
  response_time = time.time() - start_time
  # print the time delay and text received
  
  st.write(response['choices'][0]['message']['content'])

  with open(filename, 'w') as f:
    f.write(f'> system {st.session_state.system_query}, user {st.session_state.query}')
    f.write(f"< {response['choices'][0]['message']['content']}")
    f.write(f"proc time {response_time:.2f} seconds")

  st.write(f"proc time {response_time:.2f} seconds after request")
else:

  if (hasattr(st.session_state, 'last_req')):
    dt = datetime.now() - st.session_state.last_req
    if dt.total_seconds() / 60.0 < 1:
      st.write(f"Please wait a {60.0 - dt.total_seconds()} seconds" )
      exit()


  st.session_state.last_req = datetime.now()
  st.write("Process request: ", st.session_state.query)

  prompt=st.session_state.query 
  res = openai.Image.create(
    prompt=prompt,
    n=img_count,
    size="1024x1024"
  )

  tqueue = enumerate(res['data'])
  for i, rec in tqueue:
      try:
        image_url = rec["url"]
        response = requests.get(image_url)
        response.raise_for_status()

        filename = f'{root_dir}/{datetime.now().strftime("%Y%m%dT%H%M%S")}_{prompt}_{i}.png'
        with open(filename, 'wb') as f:
          f.write(response.content)
  
        image = Image.open(io.BytesIO(response.content))
        st.image(image, caption=f'{filename}', width=256)
        st.write(image_url)


      except requests.exceptions.RequestException as e:
          st.write(f'Error occurred during the request: {str(e)}')

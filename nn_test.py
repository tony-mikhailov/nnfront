import os
import openai
import requests
from datetime import datetime
from tqdm import tqdm

openai.api_key = os.getenv("OPENAI_API_KEY")

prompt="a special medical equipment from future" 
root_dir = 'NN'
res = openai.Image.create(
  prompt=prompt,
  n=5,
  size="1024x1024"
)

tqueue = tqdm(enumerate(res["data"]), desc=f'Making request "{prompt}" to Dalle...')
for i, rec in tqueue:
    try:
      resp = requests.get(rec["url"])
      resp.raise_for_status()

      filename = f'{root_dir}/{datetime.now().strftime("%Y%m%dT%H%M%S")}_{prompt}_{i}.png'
      with open(filename, 'wb') as f:
         tqueue.set_description(desc=f'save {rec["url"]} -> {filename}', refresh=True)
         f.write(resp.content)

    except requests.exceptions.RequestException as e:
        tqueue.set_description(desc=f"Error occurred during the request: {str(e)}", refresh=True)

# res = openai.Image.create_edit(
#   image=open("MELP_640_nologo.png", "rb"),
#   prompt="Fill the mask with the background, blur the background, and finish the picture with blue skyes at the top and green grass at the bottom",
#   n=1,
#   size="1024x1024"
# )

# print(res)

# print(openai.Model.list())

# for net in l.data:
#     print(net["id"])


# response = openai.Completion.create(
#   model="gpt-3.5-turbo",
#   prompt="Привет, я волшебник. Попроси меня сделать волшевство!",
#   temperature=0,
#   max_tokens=150,
#   top_p=1.0,
#   frequency_penalty=0.0,
#   presence_penalty=0.0,
#   stop=["#", ";"]
# )

# response = openai.Image.create(
#   prompt="Сгенерируй фирменный стиль для фирмы по производству озонаторов воды, ионизаторов и медицинской техники. Встиле используй небо, облака, траву и одуванчики. Используй цвета голубой, белый, зелёный и оранжевый",
#   n=1,
#   size="1024x1024"
# )

# image_url = response['data'][0]['url']

#print(l)
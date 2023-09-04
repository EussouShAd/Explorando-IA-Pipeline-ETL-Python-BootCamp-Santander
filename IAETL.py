import pandas as pd
import requests
import json
import openai


# Denição da URL da API
sdw2023_api_url = 'https://sdw-2023-prd.up.railway.app'

#API Key da OpenAI, ela será salva como uma variável de ambiente
openai_api_key = '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'

# Acessando os dados do arquivo com o Panda para um DataFrame e convertendo os IDs para uma lista.
df = pd.read_csv('SDW2023.csv')
user_ids = df['UserID'].tolist()


# Obtendo os  usuário de cada ID usando a API 

def get_user(id):
  response = requests.get(f'{sdw2023_api_url}/users/{id}')
  return response.json() if response.status_code == 200 else None

users = [user for id in user_ids if (user := get_user(id)) is not None]


# Gerando mensagens com a API do OpenAI GPT-4 

openai.api_key = openai_api_key

def generate_ai_news(user):
  completion = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
      {
          "role": "system",
          "content": "Você é um especialista em markting bancário."
      },
      {
          "role": "user",
          "content": f"Crie uma mensagem para {user['name']} sobre a importância dos investimentos (máximo de 100 caracteres)"
      }
    ]
  )
  return completion.choices[0].message.content.strip('\"')

for user in users:
  news = generate_ai_news(user)
  print(news)
  user['news'].append({
      "icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg",
      "description": news
  })


# Função para atualize a lista de "news" de cada usuário na API com a nova mensagem gerada.

def update_user(user):
  response = requests.put(f"{sdw2023_api_url}/users/{user['id']}", json=user)
  return True if response.status_code == 200 else False

for user in users:
  success = update_user(user)
  print(f"User {user['name']} updated? {success}!")

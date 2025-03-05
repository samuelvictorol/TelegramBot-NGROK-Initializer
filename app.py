from flask import Flask, request, jsonify
import json
import requests
import os
from telegram import Bot, Update
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()
app = Flask(__name__)

# Substitua pelo seu token do Telegram
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Substitua pelo seu URL do ngrok
NGROK_URL = os.getenv('NGROK_URL')

# Inicializa o bot do Telegram
bot = Bot(token=TELEGRAM_BOT_TOKEN)

@app.route('/' + TELEGRAM_BOT_TOKEN, methods=['POST'])
def webhook():
    # Recebe a requisição do Telegram (webhook)
    json_str = request.data.decode('UTF-8')
    
    # Verifica se o corpo da requisição não está vazio
    if not json_str:
        return jsonify({'error': 'Empty request body'}), 400
    
    try:
        # Tenta decodificar o JSON
        update_data = json.loads(json_str)
    except json.decoder.JSONDecodeError as e:
        return jsonify({'error': 'Invalid JSON', 'message': str(e)}), 400
    
    # Cria o objeto Update do Telegram
    update = Update.de_json(update_data, bot)
    
    # Obtém o chat_id da mensagem recebida
    chat_id = update.message.chat_id
    
    # Verifica se a mensagem é um comando '/start'
    if update.message.text == '/start':
        # Envia uma mensagem de boas-vindas ao usuário
        send_message(chat_id, "Olá, sou o bot! Como posso te ajudar?")
    else:
        # Envia uma mensagem para qualquer outra mensagem recebida
        send_message(chat_id, "Você enviou uma mensagem: " + update.message.text)

    # Imprime a mensagem recebida no console (formato JSON)
    print(json.dumps(update_data, indent=4))
    
    # Retorna uma resposta para o Telegram
    return jsonify({'status': 'ok'})


# Função para enviar mensagem usando requests
def send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    params = {
        'chat_id': chat_id,
        'text': text
    }
    response = requests.post(url, params=params)
    if response.status_code != 200:
        print(f'Erro ao enviar mensagem: {response.status_code} - {response.text}')
    else:
        print(f'Mensagem enviada para o chat_id {chat_id}: {text}')


# Função para configurar o webhook sem usar async
def set_webhook():
    webhook_url = f'{NGROK_URL}/{TELEGRAM_BOT_TOKEN}'
    # Usando requests para configurar o webhook de forma síncrona
    response = requests.get(f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/setWebhook?url={webhook_url}')
    
    if response.status_code == 200:
        print('Webhook configurado com sucesso!')
    else:
        print(f'Erro ao configurar o webhook: {response.status_code}')

if __name__ == '__main__':
    # Rodar a configuração do webhook de forma síncrona
    set_webhook()
    
    # Roda o Flask
    app.run(debug=True, host='0.0.0.0', port=5000)

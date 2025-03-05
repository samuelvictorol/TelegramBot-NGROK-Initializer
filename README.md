## Telegram Bot + NGROK

- Crie um .env com as variáveis TELEGRAM_BOT_TOKEN e NGROK_URL na raíz do projeto
- Rode o [NGROK](https://ngrok.com/downloads/windows) na porta 5000:
> ngrok http 5000
- Atribua os valores nas variáveis de ambiente: token do bot do telegram (Bot Father) e url (forwarding) do NGROK
- Instale as dependência (python 3.11) e rode o projeto
> python app.py
- Teste o bot
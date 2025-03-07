## Rodar o projeto com Docker
- [ ] Docker instalado e rodando na máquina.
- [ ] NGROK instalado e com arquivo ngrok.exe na raíz do projeto.
- [ ] rode o ngrok com o comando ngrok http 5000, copie a url forwarding e coloque na variavel de ambiente BOT_BACKEND_URL
- [ ] docker build -t seu-bot .
- [ ] docker run -p 5000:5000 seu-bot

## Exemplo de JSON retornado no webhook telegram

> "Dados recebidos":

```json
{
  "update_id": 218002779,
  "message": {
    "message_id": 105,
    "from": {
      "id": 1331214492,
      "is_bot": false,
      "first_name": "Samuel Victor",
      "username": "Samvctr",
      "language_code": "pt-br"
    },
    "chat": {
      "id": 1331214492,
      "first_name": "Samuel Victor",
      "username": "Samvctr",
      "type": "private"
    },
    "date": 1741381826,
    "text": "olá"
  }
}

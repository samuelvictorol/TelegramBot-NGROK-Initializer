const TelegramBot = require('node-telegram-bot-api');
const dotenv = require('dotenv');
const axios = require('axios');

dotenv.config();

const TELEGRAM_BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN;
const BOT_BACKEND_URL = process.env.BOT_BACKEND_URL;

// Instância do bot, apenas uma vez
const bot = new TelegramBot(TELEGRAM_BOT_TOKEN, { polling: false });

const BotController = {
    setWebhook: async () => {
        const webhookUrl = `${BOT_BACKEND_URL}/${TELEGRAM_BOT_TOKEN}`;
        try {
            const response = await axios.get(`https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/setWebhook?url=${webhookUrl}`);
            if (response.status === 200) {
                console.log('Webhook configurado com sucesso!');
            } else {
                console.error(`Erro ao configurar o webhook: ${response.status}`);
            }
        } catch (error) {
            console.error('Erro ao configurar o webhook:', error);
        }
    },

    sendMessage: async (chatId, text) => {
        try {
            const response = await axios.post(`https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage`, {
                chat_id: chatId,
                text: text
            });
            if (response.status !== 200) {
                console.error(`Erro ao enviar mensagem: ${response.status} - ${response.data}`);
            } else {
                console.log(`Mensagem enviada para o chat_id ${chatId}: ${text}`);
            }
        } catch (error) {
            console.error('Erro ao enviar mensagem:', error);
        }
    },

    webhook: async (req, res) => {
        const updateData = req.body;

        // Logando os dados recebidos para verificar o formato
        console.log('Dados recebidos:', JSON.stringify(updateData));

        if (!updateData || !updateData.message) {
            return res.status(400).json({ error: 'Mensagem não recebida corretamente' });
        }

        try {
            const { message } = updateData;
            const chatId = message.chat.id;
            const text = message.text;

            console.log(`Mensagem recebida de chat_id ${chatId}: ${text}`);

            // Verificando o comando /start
            if (text === '/start') {
                await BotController.sendMessage(chatId, 'Olá, sou o bot! Como posso te ajudar?');
            } else {
                await BotController.sendMessage(chatId, `Você enviou: ${text}`);
            }

            return res.json({ status: 'ok' });
        } catch (error) {
            console.error('Erro ao processar o webhook:', error);
            return res.status(400).json({ error: 'Erro no processamento do webhook', message: error.message });
        }
    }
}

module.exports = BotController;

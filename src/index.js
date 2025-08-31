require('dotenv').config();

const apiKey = process.env.OPENROUTER_API_KEY;
console.log("Minha chave:", apiKey);
const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const express = require('express');
const app = express();

app.use(express.json());

// Inicia cliente WhatsApp
const client = new Client({
    authStrategy: new LocalAuth()
});

client.on('qr', qr => {
    console.log('📱 Escaneie este QR Code para conectar:');
    qrcode.generate(qr, { small: true });
});

client.on('ready', () => {
    console.log('✅ WhatsApp conectado com sucesso!');
});

// API para enviar mensagens
app.post('/send', async (req, res) => {
    const { to, message } = req.body;
    try {
        await client.sendMessage(to + '@c.us', message);
        res.json({ status: 'success', to, message });
    } catch (error) {
        res.status(500).json({ status: 'error', error: error.message });
    }
});

client.initialize();

// Inicia servidor na porta 3001
app.listen(3001, () => {
    console.log('🚀 API do WhatsApp rodando em http://localhost:3001');
});

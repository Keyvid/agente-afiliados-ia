import os
import requests
from dotenv import load_dotenv

# 1. Carrega as senhas do arquivo .env
load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def enviar_mensagem_telegram(texto):
    """
    Consome a API do Telegram para enviar a mensagem formatada para o grupo.
    """
    if not TOKEN or not CHAT_ID:
        print("❌ Erro: Token ou Chat ID ausentes no arquivo .env!")
        return False

    # URL oficial da API do Telegram para envio de mensagens
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    
    # Preparamos os dados que vamos enviar (o 'payload')
    # parse_mode="Markdown" é para o Telegram entender os emojis e o negrito
    dados = {
        "chat_id": CHAT_ID,
        "text": texto,
        "parse_mode": "HTML"
    }
    
    print("📲 Enviando mensagem para o grupo do Telegram...")
    
    try:
        # Fazemos a requisição do tipo POST para o servidor do Telegram
        resposta = requests.post(url, json=dados)
        
        # Verifica se o servidor respondeu com sucesso (código 200)
        if resposta.status_code == 200:
            print("✅ Mensagem enviada com sucesso!")
            return True
        else:
            print(f"❌ Falha no envio. Código do erro: {resposta.status_code}")
            print(resposta.text)
            return False
            
    except Exception as erro:
        print(f"❌ Erro de conexão com a internet: {erro}")
        return False

# --- Bloco de Teste Isolado ---
# Só será executado se rodarmos este arquivo diretamente
if __name__ == "__main__":
    texto_teste = "🚨 **Teste de Sistema Inicializado!**\n\nSeu Cérebro de IA e seu Publicador estão conectados. O Agente de Ofertas está oficialmente online! 🤖🚀"
    enviar_mensagem_telegram(texto_teste)
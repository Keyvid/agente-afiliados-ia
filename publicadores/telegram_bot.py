import requests
import os
from dotenv import load_dotenv

load_dotenv() 

# Puxa as chaves com segurança no arquivo .env
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def enviar_mensagem_telegram(mensagem_html, url_foto):
    """
    Envia uma foto com legenda (em HTML) para o Telegram.
    Se a foto falhar, tenta enviar pelo menos o texto.
    """
    
    # Nova URL: Enviar foto
    url_api = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
    
    # O pacote que enviaremos para o servidor do Telegram
    dados = {
        "chat_id": TELEGRAM_CHAT_ID,
        "photo": url_foto,
        "caption": mensagem_html,  # O texto agora vai na legenda da foto
        "parse_mode": "HTML"       # Avisamos o Telegram para respeitar o negrito/itálico
    }

    try:
        # Enviamos tudo empacotado para o Telegram
        resposta = requests.post(url_api, data=dados)
        
        if resposta.status_code == 200:
            print("🚀 MENSAGEM COM FOTO ENVIADA PARA O TELEGRAM!")
            return True
        else:
            print(f"❌ Erro do servidor do Telegram: {resposta.text}")
            
            # Plano B: Se o link da foto estiver quebrado, a gente envia só o texto para não perder a venda
            print("Tentando enviar apenas o texto como plano B...")
            return enviar_apenas_texto(mensagem_html)

    except Exception as e:
        print(f"❌ Falha de conexão com o Telegram: {e}")
        return False

def enviar_apenas_texto(mensagem_html):
    """ Função de backup (A que usávamos antes) """
    url_api = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    dados = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mensagem_html,
        "parse_mode": "HTML"
    }
    
    try:
        resposta = requests.post(url_api, data=dados)
        return resposta.status_code == 200
    except:
        return False

# Bloco de Teste
if __name__ == "__main__":
    teste_texto = "<b>🔥 TESTE COM FOTO!</b>\n\nEssa é a versão 2.0 do robô!"
    teste_foto = "https://m.media-amazon.com/images/I/41m-Bq184fL._AC_SX522_.jpg"
    enviar_mensagem_telegram(teste_texto, teste_foto)
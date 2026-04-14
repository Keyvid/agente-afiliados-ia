import os
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Carrega as variáveis ocultas do arquivo .env com segurança
# Certifique-se de que o arquivo .env está na raiz do projeto, no mesmo nível do main.py
# (como você já confirmou que está!)
load_dotenv()

# 2. Puxa a chave da IA com segurança
CHAVE_API = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=CHAVE_API)

# 3. Define qual versão da IA vamos usar
modelo = genai.GenerativeModel('gemini-2.5-flash')

def criar_copy_vendas_curta(nome_produto, preco_antigo, preco_novo, link):
    """
    Envia os dados para o Gemini criar um texto promocional super direto e curto, modelado para grupos de ofertas.
    A porcentagem de desconto é calculada previamente no Python para garantir precisão total e velocidade.
    """
    # --- Cálculo da Porcentagem de Desconto no Python (Pre-calculation) ---
    try:
        # Pre-process prices to floats for calculation (handle commas/dots as needed for BR currency)
        # Assuming input prices come from the collector in a reliable format with commas.
        p_antigo_float = float(preco_antigo.replace(".", "").replace(",", "."))
        p_novo_float = float(preco_novo.replace(".", "").replace(",", "."))
        
        if p_antigo_float > 0:
            desconto = p_antigo_float - p_novo_float
            porcentagem = (desconto / p_antigo_float) * 100
            # Formata para 0 casas decimais para concisão, ex: "50%"
            porcentagem_str = f"{porcentagem:.0f}%" 
        else:
            porcentagem_str = "0%" # Fallback para preço antigo inválido
            
    except ValueError:
        # Fallback em caso de formatos de preço estranhos vindo do coletor
        porcentagem_str = "XX%" 
        print("⚠️ Erro ao calcular desconto. Usando 'XX%'. Verifique os formatos de preço vindo do coletor.")

    # --- Engenharia de Prompt para Copy Concisa ---
    print("🧠 IA gerando copy super rápida e direta...")

    prompt = f"""
    Atue como um especialista em marketing de afiliados para grupos de ofertas super diretas e visuais no WhatsApp/Telegram.
    Crie um texto de mensagem promocional EXATAMENTE no formato de 4 linhas abaixo, sem texto adicional. Este texto será pareado com a imagem do produto.

    DADOS DO PRODUTO (USE ESTES DADOS, NÃO INVENTE):
    - Descrição/Marca: {nome_produto}
    - Preço Antigo: R$ {preco_antigo}
    - Preço Novo: R$ {preco_novo}
    - Porcentagem de Desconto: {porcentagem_str}
    - Link: {link}

    FORMATO OBRIGATÓRIO (MÁXIMO 4 LINHAS):
    🚨 ****
    💰 ~~**R$**~~ ( OFF)
    💸 👉 **R$**
    🛍️ Compre aqui: ****
    """
    
    resposta = modelo.generate_content(prompt)
    return resposta.text

# --- Bloco de Teste Isolado Otimizado ---
# Esse código só roda se você executar este arquivo diretamente
if __name__ == "__main__":
    # Teste com dados simulados realistas
    texto_gerado_curto = criar_copy_vendas_curta(
        nome_produto="Smart TV LG 55 polegadas 4K",
        preco_antigo="3.500,00",
        preco_novo="2.199,00",
        # Simula o seu link final encurtado, como meli.la/sua-loja-tv
        link="https://meli.la/sua-loja-tv" 
    )
    
    print("\n" + "="*40)
    print("🚀 RESULTADO DA IA SUPER CONCISA:")
    print("="*40)
    print(texto_gerado_curto)
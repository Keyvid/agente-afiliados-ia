import os
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Carrega as variáveis ocultas do arquivo .env com segurança
load_dotenv()

# 2. Puxa a chave da IA com segurança
CHAVE_API = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=CHAVE_API)

# 3. Define qual versão da IA vamos usar
modelo = genai.GenerativeModel('gemini-2.5-flash')

# Adicionamos 'cupom' e 'observacao' na recepção
def gerar_texto_promocional(nome_produto, preco_antigo, preco_novo, link, cupom, observacao):
    
    # Lógica ninja do Python: Só cria a linha se você tiver digitado algo
    texto_cupom = f"\n🎟️ Use o cupom: {cupom}" if cupom.strip() else ""
    texto_obs = f"\n⚠️ Observação: {observacao}" if observacao.strip() else ""

    prompt = f"""
    Você é um especialista em vendas no Telegram. Crie uma mensagem curta e persuasiva.
    
    Produto: {nome_produto}
    Preço Antigo: {preco_antigo}
    Preço Novo: {preco_novo}{texto_cupom}{texto_obs}
    Link da oferta: {link}
    
    Regras:
    1. Seja direto e use emojis.
    2. Mostre o preço antigo e o novo.
    3. Se houver um cupom de desconto listado acima, coloque-o com muito destaque logo abaixo do Preço Novo.
    4. Se houver uma observação listada acima, coloque-a como um aviso extra logo abaixo do cupom.
    5. Coloque o link de compra no final, de forma PURA. Não use NENHUMA formatação Markdown no link (não coloque entre colchetes e parênteses). Apenas cole a URL crua no final da mensagem.
    """
    
    resposta = modelo.generate_content(prompt)
    return resposta.text

# --- Bloco de Teste Isolado Otimizado ---
# Esse código só roda se você executar este arquivo diretamente
if __name__ == "__main__":
    # Teste com dados simulados realistas
    texto_gerado_curto = gerar_texto_promocional(
        nome_produto="Smart TV LG 55 polegadas 4K",
        preco_antigo="3.500,00",
        preco_novo="2.199,00",
        # Simula o seu link final encurtado Ex.: meli.la/sua-loja-tv
        link="https://meli.la/sua-loja-tv" 
    )
    
    print("\n" + "="*40)
    print("🚀 RESULTADO DA IA SUPER CONCISA:")
    print("="*40)
    print(texto_gerado_curto)
import os
from ia.gerador_texto import gerar_texto_promocional
from publicadores.telegram_bot import enviar_apenas_texto

def extrair_nome_do_link(url):
    """
    Pega um link como: .../mochila-masculina-impermeavel/p/123...
    E transforma em: Mochila Masculina Impermeavel
    """
    try:
        # Pega só a parte do nome
        parte_nome = url.split("magazineluiza.com.br/")[1].split("/")[0]
        # Troca os tracinhos por espaços e coloca as Iniciais Maiúsculas
        return parte_nome.replace("-", " ").title()
    except:
        return "Produto em Oferta"

def rodada_de_automacao():
    print("\n" + "="*50)
    print(" 🚀 AGENTE DE OFERTAS - MODO TURBO")
    print("="*50)

    # 1. Coleta Manual Rápida
    link = input("🔗 Cole o link da Magalu: ")
    
    if not link.strip():
        print("Nenhum link fornecido. Encerrando...")
        return
        
    preco_antigo = input("❌ Qual o preço antigo? (ex: 1500,00): R$ ")
    preco_novo = input("✅ Qual o preço novo? (ex: 999,00): R$ ")

    # 2. Inteligência: Pega o nome do produto lendo a própria URL
    nome_produto = extrair_nome_do_link(link)
    print(f"\n📦 Produto identificado: {nome_produto}")

    # (O código de cima continua igual...)

    # 3. Inteligência: Pega o nome do produto lendo a própria URL
    nome_produto = extrair_nome_do_link(link)
    print(f"\n📦 Produto identificado: {nome_produto}")

    # 4. A IA entra em ação (Entregando os 4 itens separados!)
    print("\n✍️ Passando para a IA gerar a copy...")
    texto_final = gerar_texto_promocional(nome_produto, f"R$ {preco_antigo}", f"R$ {preco_novo}", link)

    # 5. Publicação
    if texto_final:
        print("\n🚀 Publicando no Telegram...")
        # Usamos a função de texto puro, para o Telegram gerar o card com a foto sozinho!
        sucesso = enviar_apenas_texto(texto_final)
        
        if sucesso:
            print("✨ SUCESSO! Oferta publicada no seu grupo!")
        else:
            print("❌ Falha ao publicar no Telegram.")

if __name__ == "__main__":
    rodada_de_automacao()
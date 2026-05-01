import os
from ia.gerador_texto import gerar_texto_promocional
from publicadores.telegram_bot import enviar_apenas_texto

def extrair_nome_do_link(url):
    try:
        parte_nome = url.split("magazineluiza.com.br/")[1].split("/")[0]
        return parte_nome.replace("-", " ").title()
    except:
        return "Produto em Oferta"

def rodada_de_automacao():
    print("\n" + "="*50)
    print(" 🚀 AGENTE DE OFERTAS - MODO TURBO CONTÍNUO")
    print("="*50)

    # O laço de repetição começa AQUI! Tudo que está com recuo (espaço) abaixo dele vai repetir.
    while True:
        print("\n" + "-"*40)
        print("Nova Oferta (ou digite 'sair' para fechar)")
        
        # 1. Coleta Manual Rápida
        link = input("🔗 Cole o link da Magalu: ")
        
        # A nossa "Porta de Saída"
        if link.strip().lower() == 'sair':
            print("\n👋 Encerrando o Agente de Ofertas. Bom descanso!")
            break  # O comando 'break' quebra o 'while' e finaliza o programa
            
        if not link.strip():
            print("❌ Nenhum link fornecido. Tente novamente.")
            continue  # O comando 'continue' ignora o resto de baixo e volta pro começo do 'while'
            
        preco_antigo = input("❌ Qual o preço antigo? (ex: 1500,00): R$ ")
        preco_novo = input("✅ Qual o preço novo? (ex: 999,00): R$ ")
        cupom = input("🎟️ Tem cupom de desconto? (Se não tiver, dê Enter): ")
        observacao = input("📝 Alguma observação? (ex: Frete grátis. Se não tiver, dê Enter): ")

        # 2. Inteligência: Pega o nome do produto
        nome_produto = extrair_nome_do_link(link)
        print(f"\n📦 Produto identificado: {nome_produto}")

        # 3. A IA entra em ação
        print("✍️ Passando para a IA gerar a copy...")
        texto_final = gerar_texto_promocional(
            nome_produto, 
            f"R$ {preco_antigo}", 
            f"R$ {preco_novo}", 
            link, 
            cupom, 
            observacao
        )

        # 4. Publicação
        if texto_final:
            print("🚀 Publicando no Telegram...")
            sucesso = enviar_apenas_texto(texto_final)
            
            if sucesso:
                print("✨ SUCESSO! Oferta publicada no seu grupo!")
            else:
                print("❌ Falha ao publicar no Telegram.")
        
        # Assim que ele termina de publicar, o 'while' recomeça lá em cima pedindo um novo link!

if __name__ == "__main__":
    rodada_de_automacao()
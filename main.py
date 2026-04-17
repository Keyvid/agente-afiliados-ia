# Importando as nossas 3 peças do quebra-cabeça
from coletores.scraper_magalu import buscar_dados_produto
from ia.gerador_texto import criar_copy_vendas_curta
from publicadores.telegram_bot import enviar_mensagem_telegram 

def executar_agente():
    print("="*50)
    print("🤖 BEM-VINDO AO SEU AGENTE DE OFERTAS 🤖")
    print("="*50)
    
    # Em vez de fixar no código, agora o Python te pede o link!
    link_oferta = input("\n🔗 Cole aqui o link do produto na Magalu: ")
    print("\n" + "-"*50)

    # ---------------------------------------------------------
    # PASSO 1: OS OLHOS (Scraper)
    # ---------------------------------------------------------
    print("▶️ PASSO 1: Acessando a loja e extraindo dados...")
    dados = buscar_dados_produto(link_oferta)

    if not dados:
        print("❌ Falha ao raspar a loja. Processo encerrado.")
        return

    # ---------------------------------------------------------
    # PASSO 2: O CÉREBRO (Inteligência Artificial)
    # ---------------------------------------------------------
    print("▶️ PASSO 2: IA formulando a copy persuasiva...")
    
    # Pegamos os dados do dicionário que o scraper retornou
    nome = dados['nome']
    de = dados['preco_antigo'] # Se você tiver alterado a chave no scraper para 'de', mude aqui
    por = dados['preco_novo']  # Se você tiver alterado a chave no scraper para 'por', mude aqui
    link = dados['link']

    # Mandamos os dados picotados para a IA trabalhar
    texto_final = criar_copy_vendas_curta(nome, de, por, link)
    
    if not texto_final:
        print("❌ A IA falhou em gerar o texto. Processo encerrado.")
        return

    print("\n📝 COPY GERADA COM SUCESSO:\n")
    print(texto_final)
    print("-" * 50)

    # ---------------------------------------------------------
    # PASSO 3: A BOCA (Publicador do Telegram)
    # ---------------------------------------------------------
    # Opcional: Uma trava de segurança para você aprovar o texto antes de postar
    confirmacao = input("\nVocê aprova essa copy? Deseja enviar para o Telegram agora? (S/N): ")
    
    if confirmacao.lower() == 's':
        print("\n▶️ PASSO 3: Enviando mensagem para o grupo...")
        sucesso = enviar_mensagem_telegram(texto_final)
        
        if sucesso:
            print("✅ OFERTA PUBLICADA COM SUCESSO!")
        else:
            print("❌ Erro ao enviar para o Telegram.")
    else:
        print("🚫 Postagem cancelada. A mensagem não foi enviada.")

if __name__ == "__main__":
    executar_agente()
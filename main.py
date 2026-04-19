import time
import schedule

from coletores.scraper_magalu import buscar_dados_produto, cacar_link_oferta_do_dia
from ia.gerador_texto import criar_copy_vendas_curta
from publicadores.telegram_bot import enviar_mensagem_telegram

def rodada_de_automacao():
    print("\n" + "="*50)
    print(" Iniciando nova busca automática de Ofertas")
    print("="*50)

    #O robo acha o link sozinho
    link_oferta = cacar_link_oferta_do_dia()

    if not link_oferta:
        print("Sem links hoje. Voltando a dormir...")
        return

    # Os olhos (Scraper extraindo dados e foto)
    print("\n Passo 1: Acessando a loja e extraindo dados...")
    dados = buscar_dados_produto(link_oferta)

    if not dados:
        print("Falha na coleta. Abortando esta rodada.")
        return

    # O Cérebro (IA)
    print("\n Passo 2: IA formulando a copy persuasiva...")
    nome = dados['nome']
    de = dados['preco_antigo']
    por = dados['preco_novo']
    link = dados['link']
    foto_do_produto = dados['foto']

    texto_final = criar_copy_vendas_curta(nome, de, por, link)

    if not texto_final:
        print("A IA falhou em gerar o texto. Abortando...")
        return

    # A boca (Telegram sem perguntar nada!)
    print("\n Passo 3: Publicando no Telegram...")
    sucesso = enviar_mensagem_telegram(texto_final, foto_do_produto)

    if sucesso:
        print("OFERTA PUBLICADA COM SUCESSO DE FORMA 100% AUTOMATÁTICA!")

    else:
        print("Erro ao enviar para o Telegram.")

# ==========================================
# O RELÓGIO (O coração da Automação)
# ==========================================
if __name__ == "__main__":
    print("🤖 SISTEMA AUTÔNOMO LIGADO. Pressione Ctrl+C para desligar.")
    
    # Para testar agora, ele vai rodar a primeira vez imediatamente
    rodada_de_automacao()
    
    # Aqui define o intervalo! (Ex: a cada 2 horas)
    schedule.every(1).hours.do(rodada_de_automacao)
    # schedule.every(30).minutes.do(rodada_de_automacao) # Opção para minutos
    
    # O laço infinito que mantém o programa vivo em segundo plano
    while True:
        schedule.run_pending()
        time.sleep(60) # O relógio checa se deu a hora a cada 60 segundos
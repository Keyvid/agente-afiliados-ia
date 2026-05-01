import time
from coletores.api_mercadolivre import cacar_oferta_ml
from ia.gerador_texto import gerar_texto_promocional
from publicadores.telegram_bot import enviar_apenas_texto

def rotina_autonoma():
    print("\n" + "="*50)
    print(" 🤖 AGENTE DE OFERTAS - PILOTO AUTOMÁTICO (ML) ")
    print("="*50)

    # 1. O robô vai buscar a oferta sozinho
    dados = cacar_oferta_ml()

    if not dados:
        print("⏭️ Nenhuma oferta encontrada nesta rodada. Tentaremos mais tarde.")
        return

    # 2. A IA entra em ação com os dados que o robô achou
    print("\n✍️ Passando para a IA gerar a copy...")
    texto_final = gerar_texto_promocional(
        dados["nome"], 
        dados["preco_antigo"], 
        dados["preco_novo"], 
        dados["link"], 
        dados["cupom"], 
        dados["observacao"]
    )

    # 3. Publicação
    if texto_final:
        print("🚀 Publicando no Telegram...")
        sucesso = enviar_apenas_texto(texto_final)
        
        if sucesso:
            print("✨ SUCESSO! Oferta do ML enviada para o grupo!")
        else:
            print("❌ Falha ao publicar no Telegram.")

if __name__ == "__main__":
    # Laço infinito do Piloto Automático
    while True:
        rotina_autonoma()
        
        # O programa "dorme" por um tempo antes de buscar outra oferta.
        # 3600 segundos = 1 hora. Ajuste conforme precisar!
        tempo_espera = 3600 
        print(f"\n💤 Missão concluída. O robô vai dormir por {tempo_espera/60:.0f} minutos...")
        time.sleep(tempo_espera)
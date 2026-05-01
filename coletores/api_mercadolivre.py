from playwright.sync_api import sync_playwright

def cacar_oferta_ml():
    print("\n🤖 Iniciando patrulha autônoma no Mercado Livre...")
    
    with sync_playwright() as p:
        # headless=False para você ver ele trabalhando (depois podemos mudar para True)
        navegador = p.chromium.launch(headless=False)
        pagina = navegador.new_page()
        
        try:
            # 1. Vai na página central de ofertas
            print("🛒 Acessando a vitrine de Ofertas do Dia...")
            pagina.goto("https://www.mercadolivre.com.br/ofertas", timeout=60000)
            
            # 2. Espera os produtos carregarem e pega o link do primeiro
            # A vírgula funciona como um "OU". Ele procura o layout novo OU o antigo.
            seletores_oferta = "a.poly-component__title, a.promotion-item__link-container, a.ui-search-item__group__element"
            pagina.wait_for_selector(seletores_oferta, timeout=15000)
            
            elemento_oferta = pagina.locator(seletores_oferta).first
            link_produto = elemento_oferta.get_attribute("href")
            
            # 3. Entra na página específica do produto
            print("📦 Produto encontrado! Entrando na página para extrair dados...")
            pagina.goto(link_produto, timeout=60000)
            

            # 4. AQUI ESTÁ A MÁGICA DO ROBÔ
            url_oficial_da_pagina = pagina.url
            link_limpo_definitivo = url_oficial_da_pagina.split("?")[0]
            
            print(f"🔗 Link Oficial Limpo e Capturado: {link_limpo_definitivo}")
            
            # Pega Título e Preços
            nome_produto = pagina.locator("h1.ui-pdp-title").first.inner_text()
            
            # Tenta pegar o preço antigo 
            try:
                
                preco_antigo_texto = pagina.locator("s.andes-money-amount .andes-money-amount__fraction").first.inner_text()
                preco_antigo = f"R$ {preco_antigo_texto}"
            except:
                preco_antigo = "" # Deixa vazio caso não encontre
                
            # Pega o preço novo exato
            preco_novo_texto = pagina.locator(".ui-pdp-price__second-line .andes-money-amount__fraction").first.inner_text()
            preco_novo = f"R$ {preco_novo_texto}"
            
            print(f"✅ Alvo confirmado: {nome_produto}")
            
            return {
                "nome": nome_produto,
                "preco_antigo": preco_antigo, 
                "preco_novo": preco_novo,
                "link": link_limpo_definitivo, # Usa o link oficial
                "cupom": "", 
                "observacao": "🔥 Oferta relâmpago no Mercado Livre!"
            }
            
        except Exception as erro:
            print(f"❌ O robô tropeçou: {erro}")
            return None
        finally:
            navegador.close()
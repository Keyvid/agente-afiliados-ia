from playwright.sync_api import sync_playwright
import re

def buscar_dados_produto(url_produto):
    print("🕵️‍♂️ Iniciando navegador disfarçado...")

    with sync_playwright() as p:
        navegador = p.chromium.launch(headless=False)
        contexto = navegador.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720}
        )
        pagina = contexto.new_page()

        try:
            print("⏳ Acessando o site...")
            pagina.goto(url_produto, timeout=60000)
            
            # O FREIO DE MÃO
            input("🛑 OLHE O NAVEGADOR! Quando o celular e o preço carregarem na tela, volte aqui e aperte ENTER...")

            # 1. Mira Sniper no Título Oficial do Produto (Hack do texto mais longo)
            try:
                # Pega todos os textos de todos os H1 da tela
                titulos_h1 = pagina.locator("h1").all_inner_texts()
                # O Python escolhe automaticamente o H1 que tem a maior quantidade de letras
                nome_produto = max(titulos_h1, key=len).strip() if titulos_h1 else "Produto em Oferta"
            except:
                nome_produto = "Produto em Oferta"

            # Função interna para limpar a sujeira dos preços usando Regex
            def limpar_preco(texto_sujo):
                # Procura apenas o padrão de dinheiro (ex: 3.239,10) no meio do texto sujo
                match = re.search(r'[\d\.]+\,\d{2}', texto_sujo)
                return match.group(0) if match else "0,00"

            # 2. Mira Sniper no Preço Novo
            try:
                preco_novo_texto = pagina.locator('[data-testid="price-value"]').first.inner_text()
                preco_novo = limpar_preco(preco_novo_texto)
            except:
                preco_novo = "0,00"

            # 3. Mira Sniper no Preço Antigo
            try:
                preco_antigo_texto = pagina.locator('[data-testid="price-original"]').first.inner_text()
                preco_antigo = limpar_preco(preco_antigo_texto)
            except:
                preco_antigo = preco_novo

            # 4. Mira Sniper na Foto Principal (ADICIONE ESTE BLOCO!)
            try:
                # Busca a etiqueta oficial de imagem da Magalu e pega o link
                url_foto = pagina.locator('[data-testid="image-default"]').first.get_attribute("src")
            except:
                # Imagem de segurança caso o site mude ou dê erro
                url_foto = "https://via.placeholder.com/400?text=Foto+Indisponivel"

            # O pacote final que é entregue ao main.py 
            return {
                "nome": nome_produto,
                "preco_antigo": preco_antigo,
                "preco_novo": preco_novo,
                "link": url_produto,
                "foto": url_foto
            }
            
        except Exception as erro:
            print(f"❌ Erro ao extrair dados da página: {erro}")
            return None
        finally:
            navegador.close()
def cacar_link_oferta_do_dia():
    """
    Acessa uma categoria específica e captura automaticamente o link de um produto.
    """
    print("🎯 Caçador ativado: Procurando a oferta do dia...")
    
    with sync_playwright() as p:
        # O Truque Ninja: Desativa a flag de automação do Chrome
        navegador = p.chromium.launch(
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )
        
        contexto = navegador.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720}
        )
        pagina = contexto.new_page()
        
        try:
            # Entrando pela porta lateral: Categoria de Celulares (menos bloqueios)
            pagina.goto("https://www.magazineluiza.com.br/celulares-e-smartphones/l/te/", timeout=60000)
            
            # Esperamos 5 segundos fingindo ser um humano lendo a tela
            pagina.wait_for_timeout(5000) 
            
            # Caçamos o primeiro link de produto
            link_bruto = pagina.locator('a[href*="/p/"]').first.get_attribute('href')
            
            if link_bruto.startswith("/"):
                link_completo = "https://www.magazineluiza.com.br" + link_bruto
            else:
                link_completo = link_bruto
                
            print(f"🔗 Produto encontrado: {link_completo}")
            return link_completo
            
        except Exception as erro:
            print(f"❌ O Caçador falhou em achar um link: {erro}")
            return None
        finally:
            navegador.close()
# --- Bloco de Teste Isolado ---
if __name__ == "__main__":
    # Link do Motorola
    link_teste = "https://www.magazineluiza.com.br/smartphone-motorola-edge-60-pro-256gb-violeta-5g-24gb-ram-67-cam-tripla-selfie-50mp/p/240170400/te/me60/?seller_id=magazineluiza&ads=patrocinado"
    
    dados = buscar_dados_produto(link_teste)
    
    print("\n" + "="*40)
    print("📦 DADOS FINAIS COLETADOS E LIMPOS:")
    print("="*40)
    if dados:
        print(f"Produto: {dados['nome']}")
        print(f"De: R$ {dados['preco_antigo']}")
        print(f"Por: R$ {dados['preco_novo']}")
        print(f"Link: {dados['link']}")
    else:
        print("Falha na coleta.")
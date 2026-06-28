import re
import subprocess
import sys
import time
from playwright.sync_api import sync_playwright

LINK_PATTERN = re.compile(r'(https?://(?:forms\.gle|docs\.google\.com/forms/d/e/)[^\s]+)')

def extrair_link(texto):
    match = LINK_PATTERN.search(texto)
    return match.group(1) if match else None

def obter_ultima_mensagem_recebida(page):
    """
    Retorna o texto da última mensagem.
    """
    # Busca todos os elementos que são mensagens
    mensagens = page.query_selector_all("div[data-testid='msg-container']")
    if not mensagens:
        return None
    # A última da lista é a mais recente (ordem DOM)
    ultima = mensagens[-1]
    # Procura o span do texto dentro dela
    span_texto = ultima.query_selector("span[data-testid='selectable-text']")
    if not span_texto:
        return None
    return span_texto.inner_text().strip()

def monitorar():
    print("🚀 Iniciando WhatsApp Web com Playwright...")
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir="./WhatsAppProfile",
            headless=False,
            args=["--no-sandbox"]
        )
        page = browser.new_page()
        page.goto("https://web.whatsapp.com")
        print("⏳ Escaneie o QR Code e aguarde o login...")
        page.wait_for_selector("div[aria-label='Lista de conversas']", timeout=120000)
        print("✅ Logado! Mantenha o chat aberto.")
        print("🔍 Monitorando novas mensagens...\n")
        
        ultimo_texto = ""
        ultimo_link = None
        
        while True:
            try:
                texto_atual = obter_ultima_mensagem_recebida(page)
                if texto_atual and texto_atual != ultimo_texto:
                    ultimo_texto = texto_atual
                    print(f"📩 Nova mensagem detectada: {texto_atual[:80]}...")
                    link = extrair_link(texto_atual)
                    if link and link != ultimo_link:
                        ultimo_link = link
                        print(f"🔗 Link do Forms: {link}")
                        print("🚀 Chamando preenchimento...")
                        subprocess.Popen([sys.executable, "autoCompleteForms.py", link])
                        browser.close()
                        time.sleep(2)  # evita repetição rápida
                time.sleep(1)
            except Exception as e:
                print(f"⚠️ Erro: {e}")
                time.sleep(5)

if __name__ == "__main__":
    monitorar()
import time
import os
from dotenv import load_dotenv
import sys
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

AUTOMATION_PROFILE_DIR = os.path.expanduser("./PerfilAutomacao")
load_dotenv('.env')

DADOS_FORMULARIO = {
    "nome_completo": os.getenv('NOME'),
    "cpf": os.getenv('CPF'),
    "tipo_utilizacao": os.getenv('TIPO_UTILIZACAO'),  
    "universidade": os.getenv('UNIVERSIDADE')
}

# =============================================================================
# FUNÇÃO PARA PREENCHER O FORMULÁRIO
# =============================================================================
def preencher_google_forms(link, dados, driver, primeiro_acesso=False):
    driver.get(link)

    if primeiro_acesso:
        input(">>> Por favor, faça o login na sua conta Google e pressione ENTER aqui para continuar...")

    wait = WebDriverWait(driver, 8)

    # --- 1. Aguardar o formulário carregar e marcar o checkbox do email ---
    try:
        checkbox = driver.find_element(By.XPATH, "//div[@role='checkbox' and contains(@aria-label, 'Registrar')]")
        if checkbox.get_attribute("aria-checked") != "true":
            checkbox.click()
            print("Checkbox do e-mail marcado.")
        else:
            print("Checkbox já marcado.")
    except Exception as e:
        print(f"Checkbox não encontrado: {e}")

    # --- 2. Preencher Nome completo ---
    try:
        inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='text']")
        if len(inputs) >= 2:
            nome = inputs[0]
            nome.clear()
            nome.send_keys(dados["nome_completo"])
    except Exception as e:
        print(f"Erro Nome: {e}")

    # --- 3. Preencher CPF ---
    try:
        inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='text']")
        if len(inputs) >= 2:
            cpf_input = inputs[1]   # segundo campo
            cpf_input.clear()
            cpf_input.send_keys(dados["cpf"])
            print("CPF preenchido (via segundo input de texto).")
        else:
            print("ERRO: Não há campos de texto suficientes para assumir o CPF.")
    except Exception as e2:
            print(f"Erro no fallback do CPF: {e2}")

    # --- 4. Selecionar Tipo de utilização (dropdown) ---
    try:
        # Localiza o elemento que abre o dropdown (contém o texto "Tipo de utilização" e depois um papel de lista)
        tipo_dropdown = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[contains(., 'Tipo de utilização')]//div[@role='listbox']")
        ))
        tipo_dropdown.click()
        time.sleep(0.8)  # pequena pausa para o menu abrir

        # Agora clica na opção desejada (ex: "Ida e volta")
        opcao = wait.until(EC.element_to_be_clickable(
            (By.XPATH, f"//div[@role='option']//span[text()='{dados['tipo_utilizacao']}']")
        ))
        opcao.click()
        print(f"Tipo de utilização selecionado: {dados['tipo_utilizacao']}")
    except Exception as e:
        print(f"Erro ao selecionar tipo de utilização: {e}")

    # --- 5. Selecionar Universidade (radio button) ---
    try:
        # Os radios têm aria-label com o nome da universidade
        radio = wait.until(EC.element_to_be_clickable(
            (By.XPATH, f"//div[@role='radio' and @aria-label='{dados['universidade']}']")
        ))
        if radio.get_attribute("aria-checked") != "true":
            radio.click()
        print(f"Universidade selecionada: {dados['universidade']}")
    except Exception as e:
        print(f"Erro na Universidade: {e}")

    # --- 6. Clicar no botão Enviar ---
    try:
        botao_enviar = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//span[text()='Enviar']//ancestor::div[@role='button']")
        ))
        botao_enviar.click()
        print("Formulário enviado com sucesso!")
        time.sleep(3)
        subprocess.run(["shutdown", "now"], check=True)
    except Exception as e:
        print(f"Erro ao clicar em Enviar: {e}")

# =============================================================================
# CONFIGURAÇÃO DO NAVEGADOR COM PERFIL REAL
# =============================================================================
def iniciar_navegador_com_perfil_automacao():
    if not os.path.exists(AUTOMATION_PROFILE_DIR):
        os.makedirs(AUTOMATION_PROFILE_DIR)
        print(f"Criando novo perfil de automação em: {AUTOMATION_PROFILE_DIR}")
    else:
        print(f"Usando perfil de automação existente em: {AUTOMATION_PROFILE_DIR}")

    chrome_options = Options()
    chrome_options.add_argument(f"--user-data-dir={AUTOMATION_PROFILE_DIR}")
    chrome_options.add_argument("--profile-directory=Default")  # Essencial para perfis
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=chrome_options)
    return driver

# =============================================================================
# EXECUÇÃO PRINCIPAL
# =============================================================================
def main(link):
    driver = iniciar_navegador_com_perfil_automacao()
    try:
        # Verifica se é a primeira execução. Você pode controlar isso com um arquivo de flag.
        is_first_run = not os.path.exists(os.path.join(AUTOMATION_PROFILE_DIR, "FirstRunDone"))
        preencher_google_forms(link, DADOS_FORMULARIO, driver, primeiro_acesso=is_first_run)
        
        # Marca que a primeira execução já ocorreu
        with open(os.path.join(AUTOMATION_PROFILE_DIR, "FirstRunDone"), 'w') as f:
            f.write("done")
            
        time.sleep(2)
    finally:
        driver.quit()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)
    link_recebido = sys.argv[1]
    main(link_recebido)
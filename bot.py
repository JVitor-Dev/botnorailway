import logging
import asyncio
import random
import os
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# Telegram API Key
API_KEY = "7748196229:AAEkbcysbmzgIiWqJyVYhEylv59mudTumEw"

# Cria pasta para screenshots
os.makedirs("prints", exist_ok=True)

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Função principal de automação
async def responder_formulario(exec_num):
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://web.solvis.net.br/s/acpo")

        # Espera inicial
        time.sleep(5)

        # 1. Selecionar "Express Mossoró"
        label = driver.find_element(By.XPATH, "//label[contains(., 'Express Mossoró')]")
        label.click()
        driver.save_screenshot(f"prints/{exec_num}_1.png")
        driver.find_element(By.XPATH, "//input[@value='Avançar']").click()

        # 2. Nota de 7 a 9
        time.sleep(5)
        nota = random.choice(["7", "8", "9"])
        driver.find_element(By.XPATH, f"//input[@value='{nota}']").click()
        driver.save_screenshot(f"prints/{exec_num}_2.png")
        driver.find_element(By.XPATH, "//input[@value='Avançar']").click()

        # 3. Escolha aleatória entre 8 opções
        time.sleep(5)
        opcoes = driver.find_elements(By.XPATH, "//input[@type='radio']")[:8]
        random.choice(opcoes).click()
        driver.save_screenshot(f"prints/{exec_num}_3.png")
        driver.find_element(By.XPATH, "//input[@value='Avançar']").click()

        # 4. Selecionar 6616544 e 6616547
        time.sleep(5)
        driver.find_element(By.XPATH, "//input[@value='6616544']").click()
        driver.find_element(By.XPATH, "//input[@value='6616547']").click()
        driver.save_screenshot(f"prints/{exec_num}_4.png")
        driver.find_element(By.XPATH, "//input[@value='Avançar']").click()

        # 5. Apenas printar e avançar
        time.sleep(5)
        driver.save_screenshot(f"prints/{exec_num}_5.png")
        driver.find_element(By.XPATH, "//input[@value='Avançar']").click()

        # 6. Selecionar 6616553 e confirmar
        time.sleep(5)
        driver.find_element(By.XPATH, "//input[@value='6616553']").click()
        driver.save_screenshot(f"prints/{exec_num}_6.png")
        driver.find_element(By.XPATH, "//input[@value='Confirmar']").click()

        driver.quit()
        return True

    except Exception as e:
        logger.error(f"[{exec_num}] Erro ao preencher: {e}")
        driver.quit()
        return False

# Comando do Telegram
async def executar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = context.args
        if not args or not args[0].isdigit():
            await update.message.reply_text("Use o comando assim: /executar 3")
            return

        vezes = int(args[0])
        await update.message.reply_text(f"Iniciando execução {vezes}x")

        for i in range(vezes):
            sucesso = await responder_formulario(i+1)
            status = "✅ Sucesso" if sucesso else "❌ Erro"
            await update.message.reply_text(f"Execução {i+1}: {status}")
            if sucesso:
                await asyncio.sleep(300)  # 5 minutos
            else:
                await asyncio.sleep(1)  # Executa próxima imediatamente

        await update.message.reply_text("🟢 Todas as execuções finalizadas.")

    except Exception as e:
        await update.message.reply_text(f"Erro: {e}")

# Inicializa bot
def main():
    app = ApplicationBuilder().token(API_KEY).build()
    app.add_handler(CommandHandler("executar", executar))
    app.run_polling()

if __name__ == "__main__":
    main()

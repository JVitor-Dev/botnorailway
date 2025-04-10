import os
import asyncio
import random
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Ativa logs no console
logging.basicConfig(level=logging.INFO)

# Variáveis de ambiente
API_KEY = os.getenv("API_KEY")
WEBHOOK_URL = "https://botnorailway-production.up.railway.app"

# Função de preenchimento do formulário
async def responder_formulario(exec_num):
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920x1080")

        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://web.solvis.net.br/s/acpo")

        # Aguarda carregamento inicial
        await asyncio.sleep(5)

        # 1. Selecionar "Express Mossoró"
        label = driver.find_element(By.XPATH, "//label[contains(., 'Express Mossoró')]")
        label.click()
        driver.save_screenshot(f"prints/{exec_num}_1.png")
        driver.find_element(By.XPATH, "//input[@value='Avançar']").click()

        # 2. Selecionar nota aleatória
        await asyncio.sleep(5)
        nota = random.choice(["7", "8", "9"])
        driver.find_element(By.XPATH, f"//input[@value='{nota}']").click()
        driver.save_screenshot(f"prints/{exec_num}_2.png")
        driver.find_element(By.XPATH, "//input[@value='Avançar']").click()

        # 3. Escolher aleatoriamente entre 8 opções
        await asyncio.sleep(5)
        opcoes = driver.find_elements(By.XPATH, "//input[@type='radio']")[:8]
        random.choice(opcoes).click()
        driver.save_screenshot(f"prints/{exec_num}_3.png")
        driver.find_element(By.XPATH, "//input[@value='Avançar']").click()

        # 4. Selecionar duas opções
        await asyncio.sleep(5)
        driver.find_element(By.XPATH, "//input[@value='6616544']").click()
        driver.find_element(By.XPATH, "//input[@value='6616547']").click()
        driver.save_screenshot(f"prints/{exec_num}_4.png")
        driver.find_element(By.XPATH, "//input[@value='Avançar']").click()

        # 5. Apenas avançar
        await asyncio.sleep(5)
        driver.save_screenshot(f"prints/{exec_num}_5.png")
        driver.find_element(By.XPATH, "//input[@value='Avançar']").click()

        # 6. Selecionar final e confirmar
        await asyncio.sleep(5)
        driver.find_element(By.XPATH, "//input[@value='6616553']").click()
        driver.save_screenshot(f"prints/{exec_num}_6.png")
        driver.find_element(By.XPATH, "//input[@value='Confirmar']").click()

        driver.quit()
        return True

    except Exception as e:
        if 'driver' in locals():
            driver.quit()
        logging.error(f"[{exec_num}] Erro: {e}")
        return False

# Comando do bot: /executar N
async def executar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = context.args
        if not args or not args[0].isdigit():
            await update.message.reply_text("Use o comando assim: /executar 3")
            return

        vezes = int(args[0])
        await update.message.reply_text(f"Iniciando execução {vezes}x...")

        for i in range(vezes):
            sucesso = await responder_formulario(i+1)
            status = "✅ Sucesso" if sucesso else "❌ Erro"
            await update.message.reply_text(f"Execução {i+1}: {status}")
            await asyncio.sleep(300 if sucesso else 1)

        await update.message.reply_text("🟢 Todas as execuções finalizadas.")

    except Exception as e:
        await update.message.reply_text(f"Erro geral: {e}")

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot no ar com webhook! Use /executar N para iniciar.")

# Função principal
def main():
    app = ApplicationBuilder().token(API_KEY).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("executar", executar))

    # Webhook configurado para Railway
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        webhook_url=WEBHOOK_URL
    )

if __name__ == "__main__":
    main()

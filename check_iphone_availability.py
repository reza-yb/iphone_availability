import time
import os
import requests
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options
import traceback

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_AVAILABILITY_CHAT_ID = os.getenv('TELEGRAM_AVAILABILITY_CHAT_ID')
TELEGRAM_DEBUG_CHAT_ID = os.getenv('TELEGRAM_DEBUG_CHAT_ID')

RESERVATION_URL = os.getenv('RESERVATION_URL')
MODEL_NAME = os.getenv('MODEL_NAME')
COLOR_NAME = os.getenv('COLOR_NAME')
CAPACITY_NAME = os.getenv('CAPACITY_NAME')

def send_telegram_message(message, chat_id):
    logging.info(f"Sending message to chat_id {chat_id}: {message}")
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'
    }
    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            logging.info(f"Message sent successfully to chat_id {chat_id}.")
        else:
            logging.error(f"Failed to send message to chat_id {chat_id}. Status code: {response.status_code}")
    except Exception as e:
        logging.error(f"Error sending message to chat_id {chat_id}: {e}")

def check_iphone_availability(driver):
    try:
        driver.get(f"{RESERVATION_URL}")
        driver.execute_script("window.localStorage.clear();")
        driver.execute_script("window.sessionStorage.clear();")
        timeout = 10

        model_button = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, f"//span[contains(text(),'{MODEL_NAME}')]"))
        )
        driver.execute_script("arguments[0].click();", model_button)
        logging.debug(f"Selected model: {MODEL_NAME}")

        color_button = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, f"//span[contains(text(),'{COLOR_NAME}')]"))
        )
        driver.execute_script("arguments[0].click();", color_button)
        logging.debug(f"Selected color: {COLOR_NAME}")

        capacity_button = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, f"//span[contains(text(),'{CAPACITY_NAME}')]"))
        )
        driver.execute_script("arguments[0].click();", capacity_button)
        logging.debug(f"Selected capacity: {CAPACITY_NAME}")

        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, "//p/button"))
        )
        message = (
            f"✅ <b>Desired iPhone is Available!</b>\n"
            f"<b>Model:</b> {MODEL_NAME}\n"
            f"<b>Color:</b> {COLOR_NAME}\n"
            f"<b>Capacity:</b> {CAPACITY_NAME}\n"
            f"<a href=\"{RESERVATION_URL}\">Click here to reserve your iPhone</a>"
        )
        send_telegram_message(message, TELEGRAM_AVAILABILITY_CHAT_ID)

    except TimeoutException:
        message = "⚠️ <b>iPhone is not available.</b>"
        send_telegram_message(message, TELEGRAM_DEBUG_CHAT_ID)
        logging.warning("iPhone is not available.")
    except WebDriverException as e:
        message = f"❌ <b>Error during script execution:</b> {e}"
        send_telegram_message(message, TELEGRAM_DEBUG_CHAT_ID)
        logging.error(f"WebDriverException encountered: {e}")
    except Exception as e:
        exc_traceback = traceback.format_exc()
        message = f"❌ <b>Unhandled Exception:</b>\n{exc_traceback}"
        send_telegram_message(message, TELEGRAM_DEBUG_CHAT_ID)
        logging.error(f"Unhandled exception: {exc_traceback}")

if __name__ == "__main__":
    send_telegram_message("🔍 Starting the iPhone availability checker...", TELEGRAM_DEBUG_CHAT_ID)
    logging.info("Starting the iPhone availability checker...")

    chrome_options = Options()
    chrome_options.binary_location = "/usr/bin/chromium"
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-cache")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        while True:
            check_iphone_availability(driver)
            time.sleep(60)
    finally:
        driver.quit()
        logging.info("Driver quit and script finished.")

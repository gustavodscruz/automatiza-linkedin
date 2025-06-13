import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def get_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
    driver = webdriver.Chrome(options=options)
    return driver

def scroll_until_end(driver, wait_time=2, max_attempts=30):
    last_height = driver.execute_script("return document.body.scrollHeight")
    attempts = 0

    while attempts < max_attempts:
        # Rola até o final da página
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(wait_time)

        # Verifica se o scroll trouxe mais conteúdo
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            print("Nenhum novo conteúdo carregado.")
            break

        last_height = new_height
        attempts += 1
        print(f"Scroll #{attempts}...")
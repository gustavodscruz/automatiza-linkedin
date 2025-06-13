from fastapi import FastAPI
from fastapi.params import Query
from pydantic import BaseModel
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = FastAPI()

class LinkedinInCredentials(BaseModel):
    email : str
    password : str

@app.get("/")
async def root():
    return {"message": "Hello World"}

def get_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
    driver = webdriver.Chrome(options=options)
    return driver

@app.get("/screenshot")
def screenshot(url : str = Query(..., description="URL to take screenshot of")):
    driver = get_driver()
    try:
        driver.get(url)
        screenshot = driver.get_screenshot_as_base64()
        return {"status" : "ok", "screenshot": screenshot}
    finally:
        driver.quit()

@app.post("/linkedin/login")
def login_linkedin(credentials : LinkedinInCredentials):
    driver = get_driver()
    try:
        driver.get("https://www.linkedin.com/login")
        wait = WebDriverWait(driver, 10)
        email_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
        email_field.send_keys(credentials.email)

        password_field = wait.until(EC.presence_of_element_located((By.ID, "password")))
        password_field.send_keys(credentials.password)

        login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Sign in']")))
        login_button.click()

        wait.until(EC.url_contains("feed"))

        screenshot_linkedin = driver.get_screenshot_as_base64()

        return {
            "status" : "sucesso",
            "mensagem" : "Login realizado com sucesso",
            "screenshot" : screenshot_linkedin
        }
    except Exception as e:
        return {"status" : "erro", "mensagem" : str(e)}
    finally:
        driver.quit()

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

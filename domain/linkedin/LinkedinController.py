from fastapi import APIRouter
from selenium.webdriver.support.wait import WebDriverWait

from domain.linkedin.LinkedinDto import LinkedinInCredentials
from utils.selenium import get_driver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


router = APIRouter(
    prefix="/linkedin",
    tags=["Linkedin"]
)

@router.post("/login")
async def login_linkedin(credentials : LinkedinInCredentials):
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

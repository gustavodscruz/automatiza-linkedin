import time
from typing import Union, List

from fastapi import APIRouter
from fastapi.params import Depends
from selenium.webdriver.support.wait import WebDriverWait
from sqlalchemy.orm import Session

from domain.linkedin.LinkedinDto import LinkedinWithUsername
from domain.linkedin.certificados.CertificadoDto import CertificadoDtoResponse, CertificadoDto
from domain.linkedin.certificados.CertificadoService import CertificadoService
from utils.database import get_db
from utils.selenium import get_driver, scroll_until_end
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

router = APIRouter(
    prefix="/certificado",
    tags=["Certificados"]
)


@router.post("/linkedin/profile",
             response_model=List[CertificadoDtoResponse],
             summary="Acessar perfil do Linkedin e listar certificados",
             response_description="Certificados do perfil")
async def view_profile(credentials: LinkedinWithUsername, db: Session = Depends(get_db)) -> Union[
    CertificadoDtoResponse, List[CertificadoDtoResponse], any]:
    driver = get_driver()
    try:
        # Primeiro fazer login
        driver.get("https://www.linkedin.com/login")
        wait = WebDriverWait(driver, 10)
        email_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
        email_field.send_keys(credentials.email)

        password_field = wait.until(EC.presence_of_element_located((By.ID, "password")))
        password_field.send_keys(credentials.password)

        login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Sign in']")))
        login_button.click()

        # Aguardar até que estejamos logados (verificando se estamos na página de feed)
        wait.until(EC.url_contains("feed"))

        driver.get(f"https://www.linkedin.com/in/{credentials.username}/")
        wait.until(EC.url_contains(credentials.username))

        licencas_section = wait.until(
            EC.presence_of_element_located((By.ID, "navigation-index-see-all-licenses-and-certifications")))
        licencas_section.click()

        wait.until(EC.url_contains("certifications"))
        time.sleep(5)

        scroll_until_end(driver)
        time.sleep(1)

        certifications_components = driver.find_elements(By.CSS_SELECTOR, '[data-view-name="profile-component-entity"]')

        components_data: List[CertificadoDto] = []

        for component in certifications_components:
            try:

                browse_map_elements = component.find_elements(By.CSS_SELECTOR, 'a[data-field="browsemap_card_click"]')

                if browse_map_elements:
                    continue

                title_element = component.find_element(
                    By.CSS_SELECTOR,
                    'div.display-flex.align-items-center.mr1.hoverable-link-text.t-bold span'
                )

                title_text = title_element.text if title_element else "Título não encontrado"

                # Buscar a div com os spans de empresa e verificação
                info_div = component.find_element(By.CSS_SELECTOR, 'div.display-flex.flex-row.justify-space-between')
                spans = info_div.find_elements(By.CSS_SELECTOR, 'span')

                verificacao = ""
                empresa = ""
                for index, span in enumerate(spans):
                    if "Verificação" in span.text:
                        empresa = spans[index - 1].text if index > 0 else "Empresa não encontrada"
                        verificacao = span.text
                        break
                    else:
                        empresa = "Empresa não encontrada"
                        verificacao = "Verificação não encontrada"

                if "\n" in verificacao:
                    verificacao = verificacao.split("\n")[0]

                credential_link = component.find_element(By.XPATH, './/a[contains(@aria-label, "Exibir credencial")]')
                credential_url = credential_link.get_attribute('href')
                components_data.append(CertificadoDto(titulo=title_text, empresa=empresa, data_validacao=verificacao,
                                                      link_url=credential_url))

            except Exception as e:
                components_data.append({"error": str(e)})

        certificado_service = CertificadoService(db)
        certificados_salvos = certificado_service.save_all(components_data)

        return certificados_salvos

    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}
    finally:
        driver.quit()

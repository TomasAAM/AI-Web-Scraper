from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
import time
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import re
import pandas as pd

def scrape_website(website):
    print('Launching chrome browser...')
    chrome_driver_path = '.\chromedriver.exe'
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service = Service(chrome_driver_path), options = options)
    
    try:
        driver.get(website)
        print('Page loaded...')
        html = driver.page_source
        
        return html
    finally:
        driver.quit()



def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""




def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    
    # Buscar todos los elementos con la clase específica
    card_content_elements = soup.find_all("div", class_="MuiCardContent-root css-1njhssi")
    
    # Extraer el texto de esos elementos
    card_texts = [element.get_text(separator="\n", strip=True) for element in card_content_elements]
    
    # Unir todos los textos encontrados con dos saltos de línea entre cada bloque de texto
    content_with_double_newlines = "\n\n".join(card_texts)
    
    return content_with_double_newlines


def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")

    # Eliminar scripts y estilos
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    # Obtener el texto y procesarlo sin eliminar saltos de línea extra
    cleaned_content = soup.get_text(separator="\n")

    # Evitar usar strip() para no eliminar saltos de línea
    #cleaned_content = "\n".join(line for line in cleaned_content.splitlines() if line)

    return cleaned_content


def cleaned_to_csv(cleaned_content):
    # Expresión regular para extraer datos
    patron = re.compile(
        r"(?P<Modelo>.+)\n"
        r"\$(?P<Precio>[\d.]+)\n"
        r"Procesador\n(?P<Procesador>.+)\n"
        r"Pantalla\n(?P<Pantalla>.+)\n"
        r"Almacenamiento\n(?P<Almacenamiento>.+)\n"
        r"Cámara\n(?P<CamaraTrasera>.+?)\s+/\s+(?P<CamaraFrontal>.+)\n"
        r"Sistema operativo\n(?P<SistemaOperativo>.+)\n"
        r"Conectividad celular\n(?P<ConectividadCelular>5G)"
    )

    # Extraer datos y convertirlos a una lista de diccionarios
    dispositivos = [m.groupdict() for m in patron.finditer(cleaned_content)]

    # Crear DataFrame
    df = pd.DataFrame(dispositivos)
    return df


def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
    ]

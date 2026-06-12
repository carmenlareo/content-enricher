import requests
from bs4 import BeautifulSoup
from src.config import WIKIPEDIA_BASE_URL, USER_AGENT


class WikipediaScraper:
    def __init__(self):

        self.headers = {'User-Agent': USER_AGENT}
        self.base_url = WIKIPEDIA_BASE_URL

    def buscar_tema(self, tema):

        url = f"{self.base_url}{tema.replace(' ', '_')}"

        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 404:
                print(f"❌ No se encontró el artículo para: {tema}")
                return None, None

            soup = BeautifulSoup(response.text, 'html.parser')


            titulo_elemento = soup.find('h1', id='firstHeading')
            titulo = titulo_elemento.text if titulo_elemento else tema


            parrafos_html = soup.find_all('p')
            parrafos = []
            for p in parrafos_html:
                texto = p.text.strip()
                if texto:
                    parrafos.append(texto)
                if len(parrafos) == 5:
                    break

            if not parrafos:
                print(f"❌ No se pudo extraer contenido de texto para: {tema}")
                return None, None

            contenido_completo = "\n\n".join(parrafos)
            return titulo, contenido_completo

        except Exception as e:
            print(f"Error al buscar el tema: {e}")
            return None, None
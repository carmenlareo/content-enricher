import requests
from bs4 import BeautifulSoup

class WikipediaScraper:
    def __init__(self):

        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        self.base_url = "https://es.wikipedia.org/wiki/"

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
            print(f"⚠️ Error al conectar con Wikipedia: {e}")
            return None, None
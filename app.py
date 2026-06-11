import os
from dotenv import load_dotenv
from scraper import WikipediaScraper
from processor import ContentProcessor

"""Lógica, Conexión API, traducción y generación de archivos,"""


class ContentEnricherApp:
    def __init__(self):

        load_dotenv()
        api_key_env = os.getenv("APIKEY_Groq")
        self.scraper = WikipediaScraper()
        self.processor = ContentProcessor(openai_key=api_key_env)

    def mostrar_menu_exportacion(self, titulo, original, enriquecido, traducido):

        print("\n==========================================")
        print("💾 OPCIONES DE EXPORTACIÓN")
        print("1. Guardar como archivo de Texto (.txt)")
        print("2. Guardar como Reporte PDF (.pdf)")
        print("3. Guardar en Ambos formatos")
        print("4. Salir sin guardar")

        opcion = input("Elige una opción (1-4): ").strip()

        if opcion in ['1', '2', '3']:
            nombre_archivo = input("📝 Ingresa el nombre para el archivo (sin extensión): ").strip()
            if not nombre_archivo:
                nombre_archivo = "reporte_final"

            if opcion == '1' or opcion == '3':
                self.processor.guardar_txt(nombre_archivo, titulo, original, enriquecido, traducido)
            if opcion == '2' or opcion == '3':
                self.processor.guardar_pdf(nombre_archivo, titulo, original, enriquecido, traducido)
        else:
            print("👋 ¡Programa finalizado sin exportar!")

    def iniciar(self):

        print("==========================================")
        print("   BIENVENIDO AL CONTENT ENRICHER AI      ")
        print("==========================================\n")

        tema = input("🔍 Ingresa el tema a buscar en Wikipedia: ").strip()
        if not tema:
            return

        idioma = input("🌐 Ingresa el idioma para la traducción (ej: EN, FR, IT): ").strip()
        if not idioma:
            return

        # Paso 1: Scraping
        titulo, contenido_original = self.scraper.buscar_tema(tema)
        if not contenido_original:
            return

        print(f"\n📄 TÍTULO ENCONTRADO: {titulo}")
        print("\n--- CONTENIDO ORIGINAL (Primeros 5 párrafos) ---")
        print(contenido_original)

        # Paso 2: IA
        contenido_enriquecido = self.processor.enriquecer_con_ia(contenido_original)
        print("\n--- CONTENIDO ENRIQUECIDO ---")
        print(contenido_enriquecido)

        # Paso 3: Traducción
        contenido_traducido = self.processor.traducir_contenido(contenido_enriquecido, idioma)
        print("\n--- CONTENIDO TRADUCIDO ---")
        print(contenido_traducido)

        # Paso 4: Exportar
        self.mostrar_menu_exportacion(titulo, contenido_original, contenido_enriquecido, contenido_traducido)
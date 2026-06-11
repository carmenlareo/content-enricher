import os
from openai import OpenAI
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

class ContentProcessor:
    def __init__(self, openai_key: str):

        self.openai_key = openai_key

        if not openai_key or openai_key == "TU_OPENAI_API_KEY":
            self.client = None
            return

        self.client = OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=self.openai_key
        )

    def enriquecer_con_ia(self, texto: str):

        print(f"\n🌐 Enriqueciendo contenido con IA (Groq)...")

        if not self.client:
            return ("[Simulación IA]: El texto sobre este tema fue expandido con datos históricos, "
                    "implicaciones tecnológicas y curiosidades culturales analizadas de forma amena.")

        prompt = f"Por favor, enriquece el siguiente texto de Wikipedia agregando contexto histórico: {texto}"

        try:

            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"[Modo Simulación por Error]: Datos enriquecidos de contingencia debido a un fallo en Groq: {e}"

    def traducir_contenido(self, texto: str, idioma_destino: str):

        print(f"\n🌐 Traduciendo contenido de forma real al idioma: {idioma_destino} (Groq)...")


        if not self.client:
            return f"[Traducción Simulada al {idioma_destino.upper()}]:\n{texto}"


        prompt = f"Traduce el siguiente texto de forma exacta al idioma cuyas siglas son '{idioma_destino}' (por ejemplo, EN es inglés, FR es francés, ES es español). Devuelve ÚNICAMENTE el texto traducido, sin comentarios adicionales:\n\n{texto}"

        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"[Modo Simulación por Error]: No se pudo traducir debido a un fallo en Groq: {e}\n\n{texto}"




    def guardar_txt(self, nombre_archivo, titulo, original, enriquecido, traducido):
        """Genera un archivo de texto plano con el reporte."""
        try:
            with open(f"{nombre_archivo}.txt", "w", encoding="utf-8") as f:
                f.write(f"=== REPORTE: {titulo} ===\n\n")
                f.write("--- CONTENIDO ORIGINAL ---\n")
                f.write(original + "\n\n")
                f.write("--- CONTENIDO ENRIQUECIDO ---\n")
                f.write(enriquecido + "\n\n")
                f.write("--- CONTENIDO TRADUCIDO ---\n")
                f.write(traducido + "\n")
            print(f"💾 Archivo de texto guardado con éxito como '{nombre_archivo}.txt'")
        except Exception as e:
            print(f"❌ Error al guardar el archivo TXT: {e}")

    def guardar_pdf(self, nombre_archivo, titulo, original, enriquecido, traducido):
        """Genera un reporte maquetado en PDF usando ReportLab."""
        try:
            doc = SimpleDocTemplate(f"{nombre_archivo}.pdf", pagesize=letter)
            styles = getSampleStyleSheet()

            estilo_titulo = ParagraphStyle('Titulo', parent=styles['Heading1'], fontSize=22, spaceAfter=20)
            estilo_sub = ParagraphStyle('Subtitulo', parent=styles['Heading2'], fontSize=14, spaceBefore=15, spaceAfter=10)
            estilo_cuerpo = ParagraphStyle('Cuerpo', parent=styles['BodyText'], fontSize=10, leading=14, spaceAfter=8)

            historia = []
            historia.append(Paragraph(f"Reporte de Investigación: {titulo}", estilo_titulo))
            historia.append(Spacer(1, 12))

            historia.append(Paragraph("1. Contenido Original (Wikipedia)", estilo_sub))
            for p in original.split('\n\n'):
                historia.append(Paragraph(p, estilo_cuerpo))

            historia.append(Paragraph("2. Contenido Enriquecido con IA", estilo_sub))
            for p in enriquecido.split('\n\n'):
                historia.append(Paragraph(p, estilo_cuerpo))

            historia.append(Paragraph("3. Contenido Traducido", estilo_sub))
            for p in traducido.split('\n\n'):
                historia.append(Paragraph(p, estilo_cuerpo))

            doc.build(historia)
            print(f"💾 Archivo PDF guardado con éxito como '{nombre_archivo}.pdf'")
        except Exception as e:
            print(f"❌ Error al guardar el archivo PDF: {e}")
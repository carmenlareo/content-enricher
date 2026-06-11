import unittest
from unittest.mock import patch, MagicMock, patch
import os

# Simulamos las importaciones de tu proyecto
# Nota: Asegúrate de que tus archivos app.py, processor.py y scraper.py estén en la misma carpeta
from app import ContentEnricherApp

class TestContentEnricherApp(unittest.TestCase):
    
    @patch('app.load_dotenv')
    @patch('app.os.getenv')
    @patch('app.WikipediaScraper')
    @patch('app.ContentProcessor')
    def test_inicializacion_exitosa_con_api_key(self, mock_processor, mock_scraper, mock_getenv, mock_load_dotenv):
        """Prueba que la aplicación se inicialice correctamente cuando existe una API Key"""
        # Configurar mocks
        mock_getenv.return_value = "gsk_faked_groq_api_key_12345"
        
        # Instanciar la app
        app = ContentEnricherApp()
        
        # Verificar comportamiento esperado
        mock_load_dotenv.assert_called_once()
        mock_getenv.assert_called_with("APIKEY_Groq")
        
        # Verificar que se crearon los componentes con los parámetros correctos
        mock_scraper.assert_called_once()
        mock_processor.assert_called_once_with(openai_key="gsk_faked_groq_api_key_12345")
        
        # Verificar asignación de atributos
        self.assertIsNotNone(app.scraper)
        self.assertIsNotNone(app.processor)

    @patch('app.load_dotenv')
    @patch('app.os.getenv')
    @patch('app.WikipediaScraper')
    @patch('app.ContentProcessor')
    def test_inicializacion_sin_api_key(self, mock_processor, mock_scraper, mock_getenv, mock_load_dotenv):
        """Prueba el comportamiento de la app si no se encuentra la API Key"""
        # Configurar mock para retornar None (no hay variable de entorno)
        mock_getenv.return_value = None
        
        # Instanciar la app
        app = ContentEnricherApp()
        
        # Verificar que de igual forma se intenta pasar None al procesador sin romper el flujo
        mock_processor.assert_called_once_with(openai_key=None)

if __name__ == '__main__':
    unittest.main()

import unittest
from unittest.mock import patch

from src.app import ContentEnricherApp

class TestContentEnricherApp(unittest.TestCase):

    @patch('src.app.load_dotenv')
    @patch('src.app.os.getenv')
    @patch('src.app.WikipediaScraper')
    @patch('src.app.ContentProcessor')
    def test_inicializacion_exitosa_con_api_key(self, mock_processor, mock_scraper, mock_getenv, mock_load_dotenv):
        mock_getenv.return_value = "gsk_faked_groq_api_key_12345"
        

        app = ContentEnricherApp()
        

        mock_load_dotenv.assert_called_once()
        mock_getenv.assert_called_with("APIKEY_Groq")
        

        mock_scraper.assert_called_once()
        mock_processor.assert_called_once_with(openai_key="gsk_faked_groq_api_key_12345")
        

        self.assertIsNotNone(app.scraper)
        self.assertIsNotNone(app.processor)

    @patch('app.load_dotenv')
    @patch('app.os.getenv')
    @patch('app.WikipediaScraper')
    @patch('app.ContentProcessor')
    def test_inicializacion_sin_api_key(self, mock_processor, mock_scraper, mock_getenv, mock_load_dotenv):

        mock_getenv.return_value = None
        

        app = ContentEnricherApp()
        

        mock_processor.assert_called_once_with(openai_key=None)

if __name__ == '__main__':
    unittest.main()

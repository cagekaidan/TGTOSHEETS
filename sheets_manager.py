import gspread
from config import GOOGLE_CREDENTIALS, GOOGLE_SHEETS_ID, GOOGLE_SHEETS_RANGE
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class SheetsManager:
    """Менеджер для работы с Google Sheets"""
    
    def __init__(self):
        self.client = None
        self.sheet = None
        self.initialize_client()
    
    def initialize_client(self):
        """Инициализирует клиент Google Sheets"""
        try:
            if not GOOGLE_CREDENTIALS:
                raise ValueError("Google credentials not available")
            
            self.client = gspread.authorize(GOOGLE_CREDENTIALS)
            self.sheet = self.client.open_by_key(GOOGLE_SHEETS_ID).sheet1
            
            # Проверяем и создаем заголовки, если таблица пустая
            self._ensure_headers()
            
            logger.info("Google Sheets client initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Google Sheets client: {e}")
            self.client = None
            self.sheet = None
    
    def _ensure_headers(self):
        """Убеждается, что в таблице есть заголовки"""
        try:
            # Получаем первую строку
            first_row = self.sheet.row_values(1)
            
            # Если первая строка пустая или не содержит нужные заголовки
            expected_headers = ["Телефон", "Email", "Имя", "Тайп"]
            
            if not first_row or first_row != expected_headers:
                # Добавляем заголовки
                self.sheet.insert_row(expected_headers, 1)
                logger.info("Headers added to the spreadsheet")
            
        except Exception as e:
            logger.error(f"Error ensuring headers: {e}")
    
    def add_row(self, data):
        """
        Добавляет строку с данными в таблицу
        
        Args:
            data (list): Список данных [телефон, email, имя, тип]
        
        Returns:
            bool: True если успешно, False в случае ошибки
        """
        if not self.sheet:
            logger.error("Google Sheets not initialized")
            return False
        
        try:
            # Добавляем временную метку для отладки
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Проверяем, что данные содержат 4 элемента
            if len(data) != 4:
                logger.error(f"Invalid data length: expected 4, got {len(data)}")
                return False
            
            # Добавляем строку в конец таблицы
            self.sheet.append_row(data)
            
            logger.info(f"Row added successfully at {timestamp}: {data}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding row to spreadsheet: {e}")
            return False
    
    def get_all_data(self):
        """
        Получает все данные из таблицы
        
        Returns:
            list: Список всех строк или None в случае ошибки
        """
        if not self.sheet:
            logger.error("Google Sheets not initialized")
            return None
        
        try:
            return self.sheet.get_all_records()
        except Exception as e:
            logger.error(f"Error getting data from spreadsheet: {e}")
            return None
    
    def clear_all_data(self):
        """
        Очищает все данные в таблице (кроме заголовков)
        
        Returns:
            bool: True если успешно, False в случае ошибки
        """
        if not self.sheet:
            logger.error("Google Sheets not initialized")
            return False
        
        try:
            # Получаем все данные
            all_values = self.sheet.get_all_values()
            
            if len(all_values) > 1:  # Если есть данные кроме заголовков
                # Очищаем все строки кроме первой (заголовки)
                range_to_clear = f"A2:D{len(all_values)}"
                self.sheet.batch_clear([range_to_clear])
                logger.info("All data cleared from spreadsheet")
            
            return True
            
        except Exception as e:
            logger.error(f"Error clearing spreadsheet: {e}")
            return False
    
    def test_connection(self):
        """
        Тестирует соединение с Google Sheets
        
        Returns:
            bool: True если соединение работает, False в противном случае
        """
        try:
            if not self.sheet:
                return False
            
            # Пытаемся получить название листа
            sheet_title = self.sheet.title
            logger.info(f"Connection test successful. Sheet title: {sheet_title}")
            return True
            
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False

import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2.service_account import Credentials as ServiceCredentials
from google_auth_oauthlib.flow import InstalledAppFlow
import json

# Telegram Bot Token (импортируется в main.py)

# Google Sheets configuration
GOOGLE_SHEETS_ID = os.getenv("GOOGLE_SHEETS_ID")
GOOGLE_SHEETS_RANGE = os.getenv("GOOGLE_SHEETS_RANGE", "Sheet1!A:D")

if not GOOGLE_SHEETS_ID:
    raise ValueError("GOOGLE_SHEETS_ID environment variable is required")

# Google Sheets API scopes
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def get_google_credentials():
    """Получает учетные данные для Google Sheets API"""
    creds = None
    
    # Попытка получить учетные данные из service account
    service_account_info = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
    if service_account_info:
        try:
            service_account_dict = json.loads(service_account_info)
            creds = ServiceCredentials.from_service_account_info(
                service_account_dict, scopes=SCOPES
            )
            return creds
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Ошибка при загрузке service account: {e}")
    
    # Fallback к OAuth2 flow (для локальной разработки)
    token_file = "token.json"
    credentials_file = "credentials.json"
    
    # Загружаем существующий токен
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    
    # Если нет валидных учетных данных, запускаем процесс авторизации
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(credentials_file):
                raise FileNotFoundError(
                    "Не найден файл credentials.json и не установлен GOOGLE_SERVICE_ACCOUNT_JSON"
                )
            
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_file, SCOPES
            )
            creds = flow.run_local_server(port=0)
        
        # Сохраняем учетные данные для следующего запуска
        with open(token_file, 'w') as token:
            token.write(creds.to_json())
    
    return creds

# Валидация конфигурации при импорте
try:
    GOOGLE_CREDENTIALS = get_google_credentials()
    print("✅ Google Sheets API credentials loaded successfully")
except Exception as e:
    print(f"❌ Error loading Google Sheets credentials: {e}")
    GOOGLE_CREDENTIALS = None

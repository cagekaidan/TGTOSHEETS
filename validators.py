import re

def validate_phone(phone):
    """
    Валидирует номер телефона
    
    Args:
        phone (str): Номер телефона для валидации
    
    Returns:
        bool: True если номер валиден, False в противном случае
    """
    if not phone:
        return False
    
    # Удаляем все пробелы, тире и скобки
    cleaned_phone = re.sub(r'[\s\-\(\)]', '', phone)
    
    # Паттерны для валидации телефонных номеров
    patterns = [
        r'^\+7\d{10}$',          # +7XXXXXXXXXX
        r'^\+\d{11,15}$',        # Международный формат
        r'^8\d{10}$',            # 8XXXXXXXXXX
        r'^7\d{10}$',            # 7XXXXXXXXXX
        r'^\d{10,11}$'           # Простой номер 10-11 цифр
    ]
    
    for pattern in patterns:
        if re.match(pattern, cleaned_phone):
            return True
    
    return False

def validate_email(email):
    """
    Валидирует адрес электронной почты
    
    Args:
        email (str): Email для валидации
    
    Returns:
        bool: True если email валиден, False в противном случае
    """
    if not email:
        return False
    
    # Паттерн для валидации email
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    return re.match(pattern, email.strip()) is not None

def validate_name(name):
    """
    Валидирует имя
    
    Args:
        name (str): Имя для валидации
    
    Returns:
        bool: True если имя валидно, False в противном случае
    """
    if not name:
        return False
    
    # Проверяем, что имя не пустое и содержит хотя бы один буквенный символ
    cleaned_name = name.strip()
    
    if len(cleaned_name) < 1:
        return False
    
    # Проверяем, что имя содержит только буквы, пробелы, тире и апострофы
    pattern = r'^[a-zA-Zа-яА-ЯёЁ\s\-\']+$'
    
    return re.match(pattern, cleaned_name) is not None

def validate_type(type_value):
    """
    Валидирует тип
    
    Args:
        type_value (str): Тип для валидации
    
    Returns:
        bool: True если тип валиден, False в противном случае
    """
    if not type_value:
        return False
    
    # Простая валидация - тип не должен быть пустым
    cleaned_type = type_value.strip()
    
    return len(cleaned_type) > 0

def format_phone(phone):
    """
    Форматирует номер телефона к стандартному виду
    
    Args:
        phone (str): Номер телефона для форматирования
    
    Returns:
        str: Отформатированный номер телефона
    """
    if not validate_phone(phone):
        return phone
    
    # Удаляем все пробелы, тире и скобки
    cleaned_phone = re.sub(r'[\s\-\(\)]', '', phone)
    
    # Если номер начинается с 8, заменяем на +7
    if cleaned_phone.startswith('8') and len(cleaned_phone) == 11:
        cleaned_phone = '+7' + cleaned_phone[1:]
    
    # Если номер начинается с 7, добавляем +
    elif cleaned_phone.startswith('7') and len(cleaned_phone) == 11:
        cleaned_phone = '+' + cleaned_phone
    
    # Если номер не начинается с +, но валиден, добавляем +7
    elif not cleaned_phone.startswith('+') and len(cleaned_phone) == 10:
        cleaned_phone = '+7' + cleaned_phone
    
    return cleaned_phone

def format_email(email):
    """
    Форматирует email к стандартному виду
    
    Args:
        email (str): Email для форматирования
    
    Returns:
        str: Отформатированный email
    """
    if not validate_email(email):
        return email
    
    return email.strip().lower()

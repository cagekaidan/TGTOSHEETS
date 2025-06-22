from enum import Enum

class UserStates(Enum):
    """Состояния пользователя в боте"""
    
    MAIN_MENU = "main_menu"
    WAITING_PHONE = "waiting_phone"
    WAITING_EMAIL = "waiting_email"
    WAITING_NAME = "waiting_name"
    WAITING_TYPE = "waiting_type"
    
    def __str__(self):
        return self.value
    
    @classmethod
    def get_all_states(cls):
        """Возвращает список всех состояний"""
        return [state.value for state in cls]
    
    @classmethod
    def is_valid_state(cls, state):
        """Проверяет, является ли состояние валидным"""
        return state in cls.get_all_states()

class UserData:
    """Класс для хранения данных пользователя"""
    
    def __init__(self):
        self.phone = ""
        self.email = ""
        self.name = ""
        self.type = ""
    
    def to_dict(self):
        """Преобразует объект в словарь"""
        return {
            "phone": self.phone,
            "email": self.email,
            "name": self.name,
            "type": self.type
        }
    
    def from_dict(self, data_dict):
        """Заполняет объект из словаря"""
        self.phone = data_dict.get("phone", "")
        self.email = data_dict.get("email", "")
        self.name = data_dict.get("name", "")
        self.type = data_dict.get("type", "")
    
    def clear(self):
        """Очищает все данные"""
        self.phone = ""
        self.email = ""
        self.name = ""
        self.type = ""
    
    def is_complete(self):
        """Проверяет, заполнены ли все поля"""
        return all([self.phone, self.email, self.name, self.type])
    
    def get_missing_fields(self):
        """Возвращает список незаполненных полей"""
        missing = []
        if not self.phone:
            missing.append("phone")
        if not self.email:
            missing.append("email")
        if not self.name:
            missing.append("name")
        if not self.type:
            missing.append("type")
        return missing
    
    def to_list(self):
        """Преобразует данные в список для записи в Google Sheets"""
        return [self.phone, self.email, self.name, self.type]
    
    def __str__(self):
        """Строковое представление объекта"""
        return f"UserData(phone='{self.phone}', email='{self.email}', name='{self.name}', type='{self.type}')"

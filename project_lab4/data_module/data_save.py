from typing import Any, Optional, List, Dict
import json
import os
import logging

class SaveData:
    """
    Класс для загрузки данных пользователей в формате JSON.

    Атрибуты:
        db_file (str): Путь к файлу базы данных. По умолчанию "BD.json".
        data (List[Dict[str, Any]]): Список данных пользователей, загруженных из файла.
        logger (logging.Logger): Логгер для записи предупреждений и ошибок.
    """
    def __init__(self, db_file: str = "BD.json"):
        """
        Инициализирует класс SaveData.

        Аргументы:
            db_file (str): Путь к файлу базы данных. По умолчанию "BD.json".
        """
        self.db_file = db_file
        self.data: List[Dict[str, Any]] = []
        self.load()
        self.logger = logging.getLogger(__name__)

    def load(self) -> None:
        """
        Загружает данные пользователей из файла базы данных.

        Если файл существует и данные могут быть загружены,
        они сохраняются в атрибуте data. В противном случае
        записывается предупреждение в лог.
        """
        if os.path.exists(self.db_file):
            with open(self.db_file, "r") as f:
                try:
                    self.data = json.load(f)
                except json.JSONDecodeError:
                    self.logger.warning("Предупреждение при загрузке данных из файла. Файл поврежден или пуст. ")
                    self.data = []

    def save(self) -> None:
        """
        Сохраняет текущие данные пользователей в файл базы данных в формате JSON.
        """
        with open(self.db_file, "w") as f:
            json.dump(self.data, f, indent=2)

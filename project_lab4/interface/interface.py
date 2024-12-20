import logging
from typing import Dict, Any, Optional, List

class UserInteraction:
    def __init__(self, load_func, save_func):
        """
        Инициализация класса UserInteraction.

        Параметры:
        ----------
        load_func : Callable
            Функция для загрузки данных пользователей.
        save_func : Callable
            Функция для сохранения данных пользователей.
        """
        self.load_func = load_func
        self.save_func = save_func
        self.data = self.load_func()
        self.logger = logging.getLogger(__name__)

    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Получает данные пользователя по его уникальному идентификатору.

        Параметры:
        ----------
        user_id : str
            Уникальный идентификатор пользователя.

        Возвращает:
        ----------
        dict или None:
            Данные пользователя, если он найден, иначе None.
        """
        for user in self.data:
            if user["user_id"] == user_id:
                return user
        return None

    def add_user(self, user_data: Dict[str, Any]) -> None:
        """
        Добавляет нового пользователя и сохраняет изменения.

        Параметры:
        ----------
        user_data : dict
            Словарь с информацией о новом пользователе.
        """
        self.data.append(user_data)
        self.save_func(self.data)
        self.logger.info(f"New user added: {user_data}")

    def update_user(self, user_id: str, updates: Dict[str, Any]) -> None:
        """
        Обновляет данные существующего пользователя.

        Параметры:
        ----------
        user_id : str
            Уникальный идентификатор пользователя.
        updates : dict
            Словарь с обновлениями для пользователя.
        """
        user = self.get_user(user_id)
        if user:
            user.update(updates)
            self.save_func(self.data)
            self.logger.info(f"User {user_id} updated with: {updates}")
        else:
            self.logger.warning(f"User with ID {user_id} not found.")

    def update_card(self, user_id: str, card_number: str, expiry_date: str = None, cvv_code: int = None, monthly_spending: Dict[str, Any] = None) -> None:
        """
        Обновляет данные карты пользователя.

        Параметры:
        ----------
        user_id : str
            Уникальный идентификатор пользователя.
        card_number : str
            Номер карты для обновления.
        expiry_date : str, optional
            Новая дата истечения срока действия карты.
        cvv_code : int, optional
            Новый CVV-код карты.
        monthly_spending : dict, optional
            Новые данные о ежемесячных расходах.
        """
        try:
            user = self.get_user(user_id)
            if user and "user_cards" in user:
                for card in user["user_cards"]:
                    if card["card_number"] == card_number:
                        if expiry_date:
                            card["expiry_date"] = expiry_date
                        if cvv_code:
                            card["cvv_code"] = cvv_code
                        if monthly_spending:
                            card["monthly_spending"] = monthly_spending
                        self.save_func(self.data)
                        self.logger.info(f"Card {card_number} updated for user {user_id}")
                        return
                self.logger.warning(f"Card {card_number} not found for user {user_id}.")
            else:
                self.logger.warning(f"User {user_id} not found or has no cards.")
        except Exception as e:
            self.logger.exception(f"An error occurred while updating the card: {e}")

    def delete_card(self, user_id: str, card_number: str) -> None:
        """
        Удаляет карту пользователя по её номеру.

        Параметры:
        ----------
        user_id : str
            Уникальный идентификатор пользователя.
        card_number : str
            Номер карты для удаления.
        """
        user = self.get_user(user_id)
        if user and "user_cards" in user:
            user_cards = user["user_cards"]
            for i, card in enumerate(user_cards):
                if card["card_number"] == card_number:
                    del user_cards[i]
                    self.save_func(self.data)
                    self.logger.info(f"Card {card_number} deleted for user {user_id}")
                    return
            self.logger.warning(f"Card {card_number} not found for user {user_id}.")
        else:
            self.logger.warning(f"User {user_id} not found or has no cards.")

    def add_card(self, user_id: str, card_number: str, expiry_date: str, cvv_code: int, monthly_spending: Dict[str, Any]) -> None:
        """
        Добавляет новую карту пользователю.

        Параметры:
        ----------
        user_id : str
            Уникальный идентификатор пользователя.
        card_number : str
            Номер новой карты.
        expiry_date : str
            Дата истечения срока действия карты.
        cvv_code : int
            CVV-код карты.
        monthly_spending : dict
            Данные о ежемесячных расходах для новой карты.
        """
        try:
            user = self.get_user(user_id)
            if user is not None:
                card_data = {
                    "card_number": card_number,
                    "expiry_date": expiry_date,
                    "cvv_code": cvv_code,
                    "monthly_spending": monthly_spending
                }
                if "user_cards" not in user:
                    user["user_cards"] = []
                user["user_cards"].append(card_data)
                self.save_func(self.data)
                self.logger.info(f"Card added for user {user_id}: {card_data}")
            else:
                self.logger.warning(f"User with ID {user_id} not found.")
        except Exception as e:
            self.logger.exception(f"An error occurred while adding the card: {e}")

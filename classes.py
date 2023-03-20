from abc import ABC, abstractmethod
import requests
from d import Connector
from datetime import datetime
class Engine(ABC):
    @abstractmethod
    def get_request(self,word,num):
        pass
    @staticmethod
    def get_connector(file_name):
        pass
class HH(Engine):
    """Данный класс создаёт запрос на API HH.ru и возвращает данные о вакансиях"""
    all = []
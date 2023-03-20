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



    def __init__(self,name=None, url=None, description=None, salary_from=None, salary_to=None, cur=None,city=None,published=None,requirements=None):
        """При инициализации класс получает несколько атрибутов , все они по умолчанию none, чтобы не передавть их  туда при объявлении клсаа
         это сделано для того чтобы записать все вакансии в список all"""

        self.name = name#название вакансии
        self.url = url#ссылка на вакансию
        self.requirements = requirements#требования к вакансии
        self.description = description#описание вакансии
        self.salary_from = salary_from#зарплата от
        self.salary_to = salary_to#зарплата до
        self.cur = cur#валюта
        self.city = city#город
        self.published = published#дата публикации



        self.all.append(self)#добавление экземпляра в список all

    @classmethod
    def get_request(cls,word:str,num:int):
        """Метод делает запрос и создаёт некоторые объекты
        при его вызове он принимает word - ключевое слово для поиска и num - номер страницы поиска
        также он создаёт новые экземпляры класса"""
        params = {'text': word, 'page': num, 'per_page': 100,}
        sourse = requests.get(f'https://api.hh.ru/vacancies?', params)
        data = sourse.json()
        for i in range(len(data['items'])):

            name = data['items'][i]['name']
            url = data['items'][i]['apply_alternate_url']
            description = data['items'][i]['snippet']['responsibility']

            if data['items'][i]['salary'] == None:
                salary_from = None
                salary_to = None
                cur = None
            else:
                salary_from = data['items'][i]['salary']['from']
                salary_to = data['items'][i]['salary']['to']
                cur = data['items'][i]['salary']['currency']
            city = data['items'][i]['area']['name']
            published = data['items'][i]['published_at']
            requirements = data['items'][i]['snippet']['requirement']

            cls(name,url,description,salary_from,salary_to,cur,city,published,requirements) #создание экземпляра класса
    def get_connector(self,job_name):
         """Получает название профессии для поиска и создаёт экземпляр класса коннектор,
         задавая название файлу с вакансиями"""
         connector = Connector()
         connector.file_name = f"{job_name}.hh.json"
         return connector
    def write_to_file(self,job_name): #записывает данные в json файл,также получает название профессии и предаёт его в метод get_connector
        con = self.get_connector(job_name)#создание экземпляра класса коннектор
        data = []#список всех вакансий , которые будут записаны в фалй
        counter = 1

        for i in self.all:
            c = {'number':counter,
                 'vacancy_name': i.name,
                 'vacancy_url': i.url,
                 'vacancy_description': i.description,
                 'vacancy_area': i.city,
                 'data_published':i.published,
                 'salary_from':i.salary_from,
                 'salary_to': i.salary_to,
                 'currency': i.cur,
                 'requirements': i.requirements}
            data.append(c)
            counter += 1
        con.insert(data) #вызов метода класса коннектор - insert для записи в файл

    def select_from_file(self,query:dict,job_name):
        """метод выбирает данные из json файла согласно значению словаря query,также получает название профессии и предаёт его в метод get_connector"""
        b = self.get_connector(job_name) #создание экземпляра класса коннектор
        vacancies = b.select(query) #вызов метода select класса connector
        counter = 1
        for i in range(len(vacancies)):
            vacancy_name = vacancies[i]["vacancy_name"]
            vacancy_url = vacancies[i]["vacancy_url"]
            vacancy_description = vacancies[i]['vacancy_description']
            vacancy_area = vacancies[i]["vacancy_area"]
            data_published = vacancies[i]["data_published"]
            salary_from = vacancies[i]['salary_from']
            salary_to = vacancies[i]['salary_to']
            currency = vacancies[i]['currency']
            requirements = vacancies[i]['requirements']
            print(f'Вакансия {counter}')
            print(f'{vacancy_name}')
            print(f'Город - {vacancy_area}')
            print(f'Зарплата от {salary_from} до {salary_to}')
            print(f'Валюта - {currency}')
            print(f'Дата публикации - {data_published}')
            print(f'Описание вакансии - {vacancy_description}')
            print(f'Требования - {requirements}')
            print()
            print()
            print()
            counter += 1

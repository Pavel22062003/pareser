from abc import ABC, abstractmethod
import requests
from connector import *

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


class SuperJob(Engine):
    """Данный класс делает запрос на api superjob, и собирает от туда информацию"""
    all = []
    file_name = 'Superjob.json'
    def __init__(self,name=None, url=None, description=None, payment_from=None, payment_to=None,city=None,date_published=None,experience=None):
        """При инициализации класс получает несколько атрибутов , все они по умолчанию none, чтобы не передавть их  туда при объявлении клсаа
                 это сделано для того чтобы записать все вакансии в список all"""

        self.name = name
        self.url = url

        self.description = description
        self.salary_from = payment_from
        self.salary_to = payment_to
        self.city = city
        self.date_published = date_published
        self.experience = experience
        self.all.append(self)
       # self.cur = cur
    @classmethod
    def get_request(cls,word,num):
        """Метод делает запрос и создаёт некоторые объекты
               при его вызове он принимает word - ключевое слово для поиска и num - номер страницы поиска,
               также он создаёт новые экземпляры класса"""
        my_auth_data = {
            'X-Api-App-Id': 'v3.r.137415525.e7fa1cf22aac8b5b10406b706ac45a9ae84c0a0e.51d59e2452670b345a8d3a578707ef7bbadfcd39'}
        request = requests.get('https://api.superjob.ru/2.0/vacancies/', headers=my_auth_data,
                                    params={"keywords": word,
                                            "page": {num}, 'count': 100}).json()
        for i in range(len(request['objects'])):
          name = request['objects'][i]['profession']  # Название вакансии
          url = request['objects'][i]['link']  # Ссылка на вакансию
          description = request['objects'][i]['candidat']  # Описание вакансии

          payment_from  = request['objects'][i]['payment_from']
          payment_to = request['objects'][i]['payment_to']
          city = request['objects'][i]['town']['title']
          ts = int(request['objects'][i]['date_published'])
          date_published = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
          experience = request['objects'][i]['experience']['title']
          cls(name, url, description, payment_from, payment_to,city,date_published,experience)

    def get_connector(self,job_name):
        """Получает название профессии для поиска и создаёт экземпляр класса коннектор,
                 задавая название файлу с вакансиями"""
        connector = Connector()
        connector.file_name = f"{job_name}.superjob.json"
        return connector
    def write_to_file(self,job_name):#записывает данные в json файл,также получает название профессии и предаёт его в метод get_connector

            con = self.get_connector(job_name)  #создание экземпляра класса коннектор
            data = []#список всех вакансий , которые будут записаны в фалй
            counter = 1

            for i in self.all:
                c = {'number':counter,
                     'vacancy_name': i.name,
                     'vacancy_url': i.url,
                     'vacancy_description': i.description,
                     'vacancy_area': i.city,
                     'data_published':i.date_published,
                     'vacancy_experience':i.experience,
                     'salary_from':i.salary_from,
                     'salary_to': i.salary_to}


                data.append(c)
                counter += 1
            con.insert(data)#вызов метода insert класса коннектор

    def select_from_file(self,query,job_name):
        """метод выбирает данные из json файла согласно значению словаря query,также получает название профессии и предаёт его в метод get_connector"""
        b = self.get_connector(job_name)
        vacancies = b.select(query)#вызов метода select , класса коннектор
        counter = 1
        for i in range(len(vacancies)):
            vacancy_name = vacancies[i]["vacancy_name"]
            vacancy_url = vacancies[i]["vacancy_url"]
            vacancy_description = vacancies[i]['vacancy_description']
            vacancy_area = vacancies[i]["vacancy_area"]
            data_published = vacancies[i]["data_published"]
            vacancy_experience = vacancies[i]["vacancy_experience"]
            salary_from = vacancies[i]['salary_from']
            salary_to = vacancies[i]['salary_to']
            print(f'Вакансия {counter}')
            print(f'{vacancy_name}')
            print(f'Город - {vacancy_area}')
            print(f'Зарплата от {salary_from} до {salary_to}')
            print(f'Дата публикации - {data_published}')
            print(f'Требуемый опыт - {vacancy_experience}')
            print(vacancy_description)
            print()
            print()
            counter += 1


from cl import *
import json

def min_salary(value,file_name):
    """Функци выводит вакансии, согласно мин требованиям по зарплате"""
    with open(file_name, encoding='UTF-8') as file:
        d = json.load(file)
        counter = 1
        for i in range(len(d)):
            if d[i]["salary_from"] is None:
                pass
            elif d[i]["salary_from"] > value:
                vacancy_name = d[i]["vacancy_name"]
                vacancy_url = d[i]["vacancy_url"]
                vacancy_description = d[i]['vacancy_description']
                vacancy_area = d[i]["vacancy_area"]
                data_published = d[i]["data_published"]
                salary_from = d[i]['salary_from']
                salary_to = d[i]['salary_to']
                currency = d[i]['currency']
                requirements = d[i]['requirements']
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


def highest_salary(file_name):
    """Функция выводит 10 самых высокооплачеваемых вакансий"""
    with open(file_name, encoding='UTF-8') as file:
        d = json.load(file)
        r = []
        for i in range(len(d)):
            if d[i]["salary_from"] is None:
                pass
            else:
                r.append(d[i])
        counter = 1
        sorted_dict = sorted(r,key=lambda x: x["salary_from"])
        for i in sorted_dict[-10:len(sorted_dict)]:
            vacancy_name = i["vacancy_name"]
            vacancy_url = i["vacancy_url"]
            vacancy_description = i['vacancy_description']
            vacancy_area = i["vacancy_area"]
            data_published = i["data_published"]

            salary_from = i['salary_from']
            salary_to = i['salary_to']
            print(f'Вакансия {counter}')
            print(f'{vacancy_name}')
            print(f'Город - {vacancy_area}')
            print(f'Зарплата от {salary_from} до {salary_to}')
            print(f'Дата публикации - {data_published}')

            print(vacancy_description)
            print()
            print()
            counter += 1


def the_newest_vacancies(file_name):
    """Функция выводит 10 самых новых вакансий"""
    with open(file_name, encoding='UTF-8') as file:
        d = json.load(file)
        r = []

        for i in range(len(d)):
            if d[i]["salary_from"] is None:
                pass
            else:
                r.append(d[i])
        sorted_dict = sorted(r,key=lambda x:x['data_published'])
        counter = 1
        for i in sorted_dict[-10:len(sorted_dict)]:
            vacancy_name = i["vacancy_name"]
            vacancy_url = i["vacancy_url"]
            vacancy_description = i['vacancy_description']
            vacancy_area = i["vacancy_area"]
            data_published = i["data_published"]

            salary_from = i['salary_from']
            salary_to = i['salary_to']
            print(f'Вакансия {counter}')
            print(f'{vacancy_name}')
            print(f'Город - {vacancy_area}')
            print(f'Зарплата от {salary_from} до {salary_to}')
            print(f'Дата публикации - {data_published}')

            print(vacancy_description)
            print()
            print()
            counter += 1

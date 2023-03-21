import os

import json


class Connector:
    """
    Класс коннектор создаёт файл , а также позваляет работать с ним

    """
    def __init__(self):
       self.__data_file = None #назавание файла

    #   self.connect_file() # вызов метода

    @property
    def file_name(self)->'file_name':
        """Возвращает название файла"""
        return self.__data_file

    @file_name.setter
    def file_name(self,value):
        """Позваляет дать название файлу"""
        self.__data_file = value

    def is_exist(self)->bool:
        """
        Метод проверяет существует ли файл
        """

        file_exist = os.path.exists(f'C:\\Users\Пользователь\PycharmProjects\Parser\{self.__data_file}')
        return file_exist



    def connect_file(self)->bool:
        """Данный метод создаёт файл в случае , если его нет"""
        if self.is_exist() == False:
            #вызывает метод is_exist и создаёт файл в зависимости от его результатов
            with open(self.__data_file, 'wb+') as file:
                 return True
        return True








    def insert(self, data)->None:
        """
        Метод проверяет является ли файл пустым и в зависимости от этого, записывает туда информацию
        """
        if self.connect_file() == True and os.path.getsize(self.__data_file) == 0:

        #if os.path.getsize(self.__data_file) == 0: #Проверка на то, является ли файл пустым

              with open(self.__data_file, 'a',encoding='UTF-8') as file:
                  json.dump(data,file,indent=2, ensure_ascii=False)




    def select(self,query:dict)->list:
        """
        Метод принимает словарь с данным от пользователя и возвращает вложеные словарь с вакансиями
        которые соответствуют критериям поиска пользователся
        """
        with open(self.__data_file,encoding='UTF-8') as file:


            file_dict = json.load(file)

            key = ''
            value = ''
            for k,v in query.items(): #распаковка переданного словаря
                key = k
                value = v

            counter = 0
            select_dict = []
            for i in range(len(file_dict)):
              if file_dict[i][key] is not None:
                  if file_dict[i][key] == value:
                      select_dict.append(file_dict[i])
        return select_dict














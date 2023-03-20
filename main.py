from utils import *
from classes import *
print('Здравствуйте!')
print('Программа имеет данные о 500 последних вакансиях с HH.ru и о 500 последних вакансиях с Superjob')
print('Хотите просмотреть вакансии?')
quest = input('Да/Нет')
if quest.lower() == 'да':
    print('Вакансии по какой профессии вы ищите? пример(Python developer)')
    job_title = input()
    print('С какого сайта вы хотите посмотреть вакансии?')
    answer = input('HH/Superjob')
    if answer.lower() == 'superjob':
        super_job = SuperJob()#создание экземпляра класса superjob
        for i in range(5):
          SuperJob.get_request(job_title, i) #парсинг 500 вакансий с api superjob
        super_job.write_to_file(job_title)#запись вакансий в файл
        while True:
          print('Вы можете посмотреть:')
          print('Вакансии с опытом работы который подходит для вас,для этого введите - Без опыта или от 1 года или от 3 лет или от 6 лет')
          print('Самые высокоплачеваемые вакансии, для этого введите -  10 самых высокооплачеваемых вакансий')
          print('Самые новые вакансии, для этого введите - 10 самых новых вакансий')
          req = input('Введите критерий для вывода информации')

          if req.lower() == 'без опыта':
            query = {'vacancy_experience' : 'Без опыта'}
            super_job.select_from_file(query,job_title)#вызов метода select_from_file класса superjob
          elif req.lower() == 'от 1 года':
               query = {'vacancy_experience': 'От 1 года'}
               super_job.select_from_file(query, job_title)
          elif req.lower() == 'от 3 лет':
               query = {'vacancy_experience': 'От 3 лет'}
               super_job.select_from_file(query, job_title)
          elif req.lower() == 'от 6 лет':
               query = {'vacancy_experience': 'От 6 лет'}
               super_job.select_from_file(query, job_title)
          elif req == '10 самых высокооплачеваемых вакансий':
               highest_salary(super_job.get_connector(job_title).file_name)#вызов функции  highest_salary куда передаётся название файла
          elif req.lower() == '10 самых новых вакансий':
              the_newest_vacancies(super_job.get_connector(job_title).file_name)#вызов функции    the_newest_vacancies куда передаётся название файла

          print('Хотите продолжить?')
          stop = input('да/нет')
          if stop == 'нет':
            break


    elif answer.lower() == 'hh' or 'hh.ru':
      hh = HH()#создание экземпляра класса hh
      for i in range(5):
        HH.get_request(job_title,i)#парсинг 500 вакансий
      hh.write_to_file(job_title)# запись их в файл
      while True:
            print('Вы можете посмотреть:')
            print('Все вакансии, для этого введите - вакансии')
            print('Посмотреть вакансии по городам, для этого просто введите слово - город')
            print('Посмотреть вакансии, в зависимости от вашей желаемой  зарплаты - для этого просто введите - зарплата')
            req = input('Введите критерий для вывода информации')
            if  req.lower() == '10 самых высокооплачеваемых вакансий':
                highest_salary(hh.get_connector(job_title).file_name)

            elif req.lower() == 'город':
                city = input('Введите название города')
                query = {"vacancy_area": city.title()}
                hh.select_from_file(query,job_title)#вызов функции the_newest_vacancies куда передаётся название файла

            elif req.lower() == 'зарплата':
                min = int(input('Введите минимальный оклад, который вам нужен, например: 15000'))
                min_salary(min,hh.get_connector(job_title).file_name)#вызов функции min_salary, куда передаётся название файла
            print('Хотите продолжить?')
            stop = input('да/нет')
            if stop == 'нет':
                break
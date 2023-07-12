from abc import ABC, abstractmethod
import requests
import json
import os


class working_with_API(ABC):
    '''Созадл класс наследующийся от обстактного'''

    @abstractmethod
    def get_data_from_API(self, user_request):
        '''Обязую классы наследники создавать этот метод'''
        pass


class HeadHunterAPI(working_with_API):
    def __init__(self, user_request):
        self.user_request = user_request

    def get_data_from_API(self):
        '''Метод получения данных по API'''
        v_hh = []
        URL = 'https://api.hh.ru/vacancies'
        for page in range(1, 11):
            params = {
                'per_page': 100,
                'area': 113,
                'page': page,
                'text': self.user_request,
                'only_with_salary': True
            }
            response = requests.get(URL, params=params).json()
            v_hh.extend(response['items'])
        return v_hh

    def formated_vacancies(self):
        '''Этот метод создает из полученных данных спосок с только нужными нам позициями взятыми из вакансии'''
        hh_vacancies = []
        for vacanc in self.get_data_from_API():
            hh_vacancies.append({
                'title': vacanc['name'],
                'salary_from': vacanc['salary']['from'],
                'description': vacanc['snippet']['responsibility'],
                'url': vacanc['apply_alternate_url']
            })
        return hh_vacancies


class superjob_ru(working_with_API):
    def __init__(self, user_request):
        self.user_request = user_request

    def get_data_from_API(self):
        '''Метод получения данных по API'''
        v = []
        URL = 'https://api.superjob.ru/2.0/vacancies/'
        SUPERJOB_API_KEY = os.environ.get('SUPERJOB_API_KEY')
        headers = {'X-Api-App-Id': SUPERJOB_API_KEY}
        for page in range(1, 11):
            params = {
                'count': 100,
                'page': page,
                'keyword': self.user_request,
                'archive': False
            }
            response = requests.get(URL, headers=headers, params=params).json()
            v.extend(response['objects'])
        return v

    def formated_vacancies(self):
        '''Этот метод создает из полученных данных спосок с только нужными нам позициями взятыми из вакансии'''
        vacancies = []
        for vacanc in self.get_data_from_API():
            vacancies.append({
                'title': vacanc['profession'],
                'salary_from': vacanc['payment_from'],
                'description': vacanc['firm_activity'],
                'url': vacanc['link']
            })
        return vacancies


class Vacancy():
    def __init__(self, vacancy):
        self.title = vacancy['title']
        if not isinstance(vacancy['salary_from'], int):
            self.salary_from = 0
        else:
            self.salary_from = vacancy['salary_from']
        self.description = vacancy['description']
        self.url = vacancy['url']

    def __gt__(self, other):
        '''Метод сравнения экзепляров класса по зарплате '''
        sc = other if isinstance(other, int) else other.salary_from
        return self.salary_from > sc

    def __str__(self):
        return f'{self.title}\n Зарплата от {self.salary_from}\n{self.url}\nОписание:{self.description}'


class JSONSaver():
    def __init__(self, filename='vacancy.json'):
        self.filename = filename

    def file_creation(self, vac):
        '''Записывает в файл отформатированные вакансии'''
        with open(self.filename, 'w', encoding='utf8') as f:
            json.dump(vac, f, indent=2, ensure_ascii=False)

    def output_all(self):
        '''Метод для вывевдения всех полученых вакансий в виде экзепляров класса Vacancy()'''
        with open(self.filename, 'r', encoding='utf8') as file:
            data = json.load(file)
            vacancy_data = [Vacancy(x) for x in data]
        return vacancy_data

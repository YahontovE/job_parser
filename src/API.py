from abc import ABC, abstractmethod
import requests
import json
import os


class working_with_API(ABC):
    @abstractmethod
    def get_data_from_API(self,user_request):
        pass


class HeadHunterAPI(working_with_API):
    def get_data_from_API(self):
        req = requests.get('https://api.hh.ru/vacancies?only_with_salary=true&area=113&per_page=100').json()
        # for i in req['items']:
        #    print(i)
        return req


class superjob_ru(working_with_API):
    def __init__(self, user_request):
    #    self.v = []
        self.user_request = user_request

    def get_data_from_API(self):
        v=[]
        URL = 'https://api.superjob.ru/2.0/vacancies/'
        SUPERJOB_API_KEY = os.environ.get('SUPERJOB_API_KEY')
        headers = {'X-Api-App-Id': SUPERJOB_API_KEY}
        for page in range(1,11):
            params = {
                'count': 100,
                'page': page,
                'keyword': self.user_request,
                'archive': False
                # 'payment_from': True
            }
            response = requests.get(URL, headers=headers, params=params).json()
            # sas=response.content.decode()
            # js=json.dumps(response,indent=2,ensure_ascii=False)
            # data = json.loads(js)
            # print(response['total'])
            # print(response['total'])
            v.extend(response['objects'])
        return v

    def formated_vacancies(self):
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
    def __init__(self,vacancy):
        self.title =vacancy['title']
        self.salary_from =vacancy['salary_from']
        self.description =vacancy['description']
        self.url =vacancy['url']

    def __gt__(self, other):
        return self.salary_from > other.salary_from
    def __str__(self):
        return f'{self.title}\n Зарплата от {self.salary_from}\n{self.url}\nОписание:{self.description}'


class JSONSaver():
    def __init__(self, filename='vacancy.json'):
        self.filename = filename


    def file_creation(self, vac):
        with open(self.filename, 'w', encoding='utf8') as f:
            json.dump(vac, f, indent=2, ensure_ascii=False)

    def output_all(self):
        with open(self.filename, 'r', encoding='utf8') as file:
            data = json.load(file)
            vacancy_data=[Vacancy(x) for x in data]
        return vacancy_data


class Processing_Vacancies(HeadHunterAPI):
    def __init__(self):
        self.name = self.get_data_from_API()['items'][0]['name']

    def get(self):
        with open('data.json', 'w', encoding='utf8') as file:
            page = 0
            while page < 10:
                url = f'https://api.hh.ru/vacancies?only_with_salary=true&area=113&page={page}&per_page=100'
                data = requests.get(url).json()
                file.write(json.dumps(data, ensure_ascii=False))
                page += 1
                # for i in self.get_data_from_API()['items']:
                #    print(i)

# a=HeadHunterAPI()
# print(a.get_data_from_API())
# q=Processing_Vacancies()
# print(q.name)
# w = superjob_ru()
# w.get_data_from_API('Python developer')
# w.get_data_from_API()
# print(w.get_data_from_API('ьааал'))
# print(w.formated_vacancies())
#js=JSONSaver('Врач',[])
#print(js.output_all())
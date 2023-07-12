
import src.API


def main():
    # Получение ваканский
    user_request = input('Введите название вакансии ')
    source = int(input('Введите число для получения вакансий:\n1-hh.ru\n2-SuperJob\n3-Получить с обоих\n'))
    sj = src.API.superjob_ru(user_request)
    hh = src.API.HeadHunterAPI(user_request)
    if source == 1:
        a = [hh]
    if source == 2:
        a = [sj]
    if source == 3:
        a = [hh, sj]

    vac = []
    for api in a:
        api.get_data_from_API()
        vac.extend(api.formated_vacancies())

    # Сохранение вакансий
    js = src.API.JSONSaver()
    js.file_creation(vac)
    # Вывод
    while True:
        num = int(input('1-вывести все,2-Сортировать по зарплате 3-Выход\n'))
        if num == 1:
            n = js.output_all()
            for i in n:
                print(i)
        if num == 2:
            n = js.output_all()
            for i in sorted(n, reverse=True):
                print(i)
        if num == 3:
            break



if __name__ == '__main__':
    main()

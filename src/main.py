# from src.API import superjob_ru
import src.API


def main():
    # Получение ваканский
    user_request = input('Введите название вакансии ')
    source = int(input('Введите число для получения вакансий:\n1-hh.ru\n2-SuperJob\n'))
    # hh=src.API.HeadHunterAPI(user_request)
    sj = src.API.superjob_ru(user_request)
    if source == 1:
        a = [hh]
    if source == 2:
        a = [sj]

    vac = []
    for api in a:
        api.get_data_from_API()
        vac.extend(api.formated_vacancies())


    # Сохранение вакансий
    js = src.API.JSONSaver()
    js.file_creation(vac)
    #vac = []
    while True:
        num = int(input('1-вывести все, 2-Выход '))
        if num == 1:
            n = js.output_all()
        if num == 2:
            break


        for i in n:
            print(i)


if __name__ == '__main__':
    main()

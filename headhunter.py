import requests
from itertools import count


def predict_rub_salary_for_headhunter(salary_from=None, salary_to=None):
    if salary_from and salary_to:
        average_salary = (salary_from+salary_to)/2
    elif salary_from:
        average_salary = salary_from*1.2
    elif salary_to:
        average_salary = salary_to*0.8
    else:
        average_salary = None
    return average_salary


def get_vacancies(language='Python', page=0, city_id=1, period=30):
    url = 'https://api.hh.ru/vacancies'
    params = {
        'text': f'Программист {language}',
        'area': city_id,
        'period': period,
        'page': page
    }
    response = requests.get(url, params)
    return response.json()


def get_statistics_vacancies(language):
    average_salaries = []
    for page in count(0):
        vacancies = get_vacancies(language, page)
        if page >= vacancies['pages']-1:
            break
        for salary_item in vacancies['items']:
            if not salary_item['salary']:
                continue
            if not salary_item['salary']['currency'] == 'RUR':
                continue
            average_salaries.append(predict_rub_salary_for_headhunter(salary_item['salary']['from'], salary_item['salary']['to']))
    vacancies_processed = len(average_salaries)
    average_salary = int(sum(average_salaries)/vacancies_processed)
    statistics_vacancies = {
        "vacancies_found": vacancies['found'],
        "vacancies_processed": vacancies_processed,
        "average_salary": average_salary
    }
    return statistics_vacancies


def get_statistics_languages_hh(programming_languages):
    statistics_languages = {}
    for language in programming_languages:
        statistics_languages[language] = get_statistics_vacancies(language)
    return statistics_languages



from itertools import count

import requests

from predict_salary import predict_rub_salary

def get_vacancies(language='Python', page=0, city_id=1, period=30):
    url = 'https://api.hh.ru/vacancies'
    params = {
        'text': f'Программист {language}',
        'area': city_id,
        'period': period,
        'page': page
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
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
            average_salaries.append(predict_rub_salary(salary_item['salary']['from'], salary_item['salary']['to']))
    if average_salaries:
        vacancies_processed = len(average_salaries)
        average_salary = int(sum(average_salaries)/vacancies_processed)
    else:
        vacancies_processed = None
        average_salary = None
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



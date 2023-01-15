import os
from collections import defaultdict
from itertools import count

import requests
from dotenv import load_dotenv

from predict_salary import predict_rub_salary


def get_vacancies(language='Python', page=0, town_id=4, catalogues=48, period=30):
    load_dotenv()
    superjob_key = os.getenv('SUPERJOB_KEY')
    url = 'https://api.superjob.ru/2.0/vacancies'
    headers = {
        'X-Api-App-Id': superjob_key
    }
    params = {
        'town': town_id,
        'catalogues': catalogues,
        'keyword': language,
        'page': page,
        'period': period
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()


def get_statistics_vacancies(language):
    average_salaries = []
    for page in count(0, 1):
        vacancies = get_vacancies(language, page)
        for vacancy in vacancies['objects']:
            if not vacancy["payment_from"] and not vacancy["payment_to"] or not vacancy["currency"] == "rub":
                continue
            average_salaries.append(predict_rub_salary(vacancy['payment_from'], vacancy['payment_to']))
        if not vacancies['more']:
            break
    vacancies_processed = len(average_salaries)
    if vacancies_processed:
        average_salary = int(sum(average_salaries)/vacancies_processed)
    else:
        average_salary = None
    statistics_vacancies = {
        "vacancies_found": vacancies['total'],
        "vacancies_processed": vacancies_processed,
        "average_salary": average_salary
    }
    return statistics_vacancies


def get_statistics_languages_sj(programming_languages):
    statistics_languages = defaultdict()
    for language in programming_languages:
        statistics_languages[language] = get_statistics_vacancies(language)
    return statistics_languages


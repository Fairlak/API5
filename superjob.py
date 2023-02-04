import os
from collections import defaultdict
from itertools import count

import requests


from predict_salary import predict_rub_salary


def get_vacancies(superjob_key, language='Python', page=0, town_id=4, catalogues=48, period=30):
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
    response.raise_for_status()
    return response.json()


def get_vacancies_statistics(language, superjob_key):
    average_salaries = []
    for page in count(0, 1):
        vacancies = get_vacancies(superjob_key, language, page)
        for vacancy in vacancies['objects']:
            if not vacancy["payment_from"] and not vacancy["payment_to"] or not vacancy["currency"] == "rub":
                continue
            average_salaries.append(predict_rub_salary(vacancy['payment_from'], vacancy['payment_to']))
        if not vacancies['more']:
            break
    if average_salaries:
        vacancies_processed = len(average_salaries)
        average_salary = int(sum(average_salaries)/vacancies_processed)
    else:
        vacancies_processed = None
        average_salary = None
    statistics_vacancies = {
        "vacancies_found": vacancies['total'],
        "vacancies_processed": vacancies_processed,
        "average_salary": average_salary
    }
    return statistics_vacancies


def get_statistics_languages_sj(programming_languages, superjob_key):
    languages_statistics = defaultdict()
    for language in programming_languages:
        languages_statistics[language] = get_vacancies_statistics(language, superjob_key)
    return languages_statistics


import os
import requests
from itertools import count
from dotenv import load_dotenv
from collections import defaultdict



def get_superjob_vacancies(language='Python', page=0, town_id=4, catalogues=48, period=30):
    load_dotenv()
    secret_key = os.getenv('SECRET_KEY')
    url = 'https://api.superjob.ru/2.0/vacancies'
    headers = {
        'X-Api-App-Id': secret_key
    }
    params = {
        'town': town_id,
        'catalogues': catalogues,
        'keyword': language,
        'page': page,
        'period': period
    }
    response = requests.get(url, headers=headers, params=params)
    superjob_programmers = response.json()
    return superjob_programmers


def predict_rub_salary_for_superJob(payment_from=None, payment_to=None):
        if payment_from and payment_to:
            average_salary = (payment_from + payment_to) / 2
        elif payment_from:
            average_salary = payment_from * 1.2
        elif payment_to:
            average_salary = payment_to * 0.8
        return average_salary


def get_statistics_vacancies(language):
    average_salaries = []
    for page in count(0, 1):
        vacancies = get_superjob_vacancies(language, page)
        for vacancy in vacancies['objects']:
            if not vacancy["payment_from"] and not vacancy["payment_to"] or not vacancy["currency"] == "rub":
                continue
            average_salaries.append(predict_rub_salary_for_superJob(vacancy['payment_from'], vacancy['payment_to']))
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


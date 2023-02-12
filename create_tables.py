import os

from dotenv import load_dotenv
from terminaltables import AsciiTable

from superjob import get_statistics_languages_sj
from headhunter import get_statistics_languages_hh




def create_table(statistics_languages, title):
    table_header = [
        ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']
        ]
    for language, vacancy in statistics_languages.items():
        table_content = [
            language,
            vacancy['vacancies_found'],
            vacancy['vacancies_processed'],
            vacancy['average_salary']
        ]
        table_header.append(table_content)
        table_instance = AsciiTable(table_header, title)
        table_instance.justify_columns[2] = 'left'
    return table_instance.table


def main():
    load_dotenv()
    superjob_key = os.getenv('SUPERJOB_KEY')
    programming_languages = [
        'JavaScript',
        'Java',
        'Python',
        'Ruby',
        'PHP',
        'C++',
        'C',
        'Go'
    ]
    sj_languages_statistics = get_statistics_languages_sj(programming_languages, superjob_key)
    print(create_table(sj_languages_statistics, title='SuperJob Moscow'))
    hh_languages_statistics = get_statistics_languages_hh(programming_languages)
    print(create_table(hh_languages_statistics, title='Headhunter Moscow'))



if __name__ == "__main__":
    main()


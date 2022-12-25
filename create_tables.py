from superjob import get_statistics_languages_sj
from headhunter import get_statistics_languages_hh
from terminaltables import AsciiTable


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


def create_table(statistics_languages, title):
    table = [
        ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']
        ]
    for language, vacancy in statistics_languages.items():
        table_data = [
            language,
            vacancy['vacancies_found'],
            vacancy['vacancies_processed'],
            vacancy['average_salary']
        ]
        table.append(table_data)
        table_instance = AsciiTable(table, title)
        table_instance.justify_columns[2] = 'left'
    print(table_instance.table)


def main():
    statistics_languages_sj = get_statistics_languages_sj(programming_languages)
    create_table(statistics_languages_sj, title='SuperJob Moscow')
    statistics_languages_hh = get_statistics_languages_hh(programming_languages)
    create_table(statistics_languages_hh, title='Headhunter Moscow')


if __name__ == "__main__":
    main()


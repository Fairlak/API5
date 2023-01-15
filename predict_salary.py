
def predict_rub_salary(salary_from=None, salary_to=None):
    if salary_from and salary_to:
        average_salary = (salary_from+salary_to)/2
    elif salary_from:
        average_salary = salary_from*1.2
    elif salary_to:
        average_salary = salary_to*0.8
    else:
        average_salary = None
    return average_salary

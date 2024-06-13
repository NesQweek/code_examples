import os
import pandas as pd
import json
import dill
import random
import string


# Директория контейнера
#path = '/opt/airflow'
# Локальная директория
path = os.getcwd()


test_folder = path + '/data/test'
models_folder = path + '/data/models'
test_json_path = f'{test_folder}/test.json'

df = pd.read_csv(f'{path}/data/train/loan_data_set.csv')


def generate_random_string(length):
    alphanumeric_chars = string.ascii_letters + string.digits
    return ''.join(random.choices(alphanumeric_chars, k=length))

def generate_random_number(length):
    return random.randint(0, 10**length - 1)

def generate_random_dataJSON():
    Loan_ID = 'LP00' + str(generate_random_number(4))
    Gender = random.choice(['Male', 'Female'])
    Married = random.choice(['Yes', 'No'])
    Dependents = random.choice(range(1,4))
    Education = random.choice(['Graduate', 'Not Graduate'])
    Self_Employed = random.choice(['Yes', 'No'])
    ApplicantIncome = generate_random_number(random.choice(range(3,6)))
    CoapplicantIncome = float(generate_random_number(random.choice(range(5))))
    LoanAmount = float(generate_random_number(random.choice(range(1,4))))
    Loan_Amount_Term = float(generate_random_number(random.choice(range(2,4))))
    Credit_History = random.choice([1.0, 0.0])
    Property_Area = random.choice(['Semiurban', 'Urban', 'Rural'])
    Loan_Status = random.choice(['Y', 'N'])

    data = {'Loan_ID': Loan_ID,
            'Gender': Gender,
            'Married': Married,
            'Dependents': Dependents,
            'Education': Education,
            'Self_Employed': Self_Employed,
            'ApplicantIncome': ApplicantIncome,
            'CoapplicantIncome': CoapplicantIncome,
            'LoanAmount': LoanAmount,
            'Loan_Amount_Term': Loan_Amount_Term,
            'Credit_History': Credit_History,
            'Property_Area': Property_Area,
            'Loan_Status': Loan_Status
            }

    return data


data = generate_random_dataJSON()


# with open(test_json_path, 'w') as file:
#     json.dump(data, file, indent=4)

    

# import dill
# path = models_folder + '/loan_predict.pkl'

# with open(path, 'rb') as file:
#     model = dill.load(file)
#     pred = model.predict(data)
#     print(pred)

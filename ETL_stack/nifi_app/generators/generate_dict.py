import random
import string

def generate_random_string(length):
    alphanumeric_chars = string.ascii_letters + string.digits
    return ''.join(random.choices(alphanumeric_chars, k=length))

def generate_random_number(length):
    return random.randint(0, 10**length - 1)

def generate_random_data_dict():
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


if __name__=='__main__':
    generate_random_data_dict()
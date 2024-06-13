
import requests
import json

# Предположим, что у нас есть переменные с результатами из первого и второго процессов
loan_id = '6325'
predict = 0.75

# Создаем словарь с данными для отправки
data = {
    'loan_id': loan_id,
    'predict': predict
}

# Отправляем POST запрос на адрес localhost:8000/api/airflow
url = 'http://localhost:8000/api/airflow/'
response = requests.post(url, data=json.dumps(data), headers={'Content-Type': 'application/json'})

if response.status_code == 200:
    print("Prediction added successfully")
else:
    print("Failed to add prediction")
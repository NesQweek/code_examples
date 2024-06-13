from django.shortcuts import render

from django.http import HttpResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from api_predictions.models import Prediction

@api_view(['POST'])
def add_prediction(request):
    loan_id = request.data.get('loan_id')
    predict = request.data.get('predict')

    prediction = Prediction(loan_id=loan_id, predict=predict)
    prediction.save()
    
    return Response("Prediction added successfully")




def home(request):
    
    return HttpResponse('Информация по запросам по адресу /info')

   
def info(request):
    
    return HttpResponse(""" 
<p>
    Доступ в /admin -> login: admin, password: openfukingweb
</p>
<p>
    Доступ в Airflow -> login: airflow, password: airflow
</p>

<p>
    ___________________________________________________________________________________________________
</p>


<p>  
    1. В этой реализации JSON записи поступают из ETL конвейера Nifi, который непрерывно собирает их с брокеров,
</p>
<p>
    данные на брокеры генерируются (имитация внешних продюсеров) и поступают по расписанию в Airflow 
</p>
<p>
    Затем эти JSON записи по расписанию скармливаются ансамблю ML моделей, которые совместно выносят прогноз,
</p>
<p>  
     который является решением по кредиту и затем прогноз отправляется в веб-приложение
</p>
<p>  
    Все результаты можно посмотреть через админку по адресу /admin
</p>
    ___________________________________________________________________________________________________
<p>
    2. Либо можно подать JSON данные самому: 
</p>
<p>
    Для отправки по API POST запроса с предсказанием модели по ипотечному кредитованию,
</p>
<p>
    полученного из Airflow, данные нужно подать в виде .json на URL 'http://localhost:8000/api/airflow/'
</p>
<p>
    Пример запроса:
    response = requests.post(URL, data=from_airflow.json, headers={'Content-Type': 'application/json'})
</p>



""")

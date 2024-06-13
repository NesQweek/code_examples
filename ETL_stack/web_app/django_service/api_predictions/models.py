from django.db import models


class Prediction(models.Model):
    loan_id = models.CharField(max_length=10)
    predict = models.FloatField()
    predict_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Идентификатор: {self.loan_id} / Предсказание: {self.predict} / Время: {self.predict_time}'
        

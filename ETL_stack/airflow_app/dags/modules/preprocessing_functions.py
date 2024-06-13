import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin


def drop_id(df: pd.DataFrame) -> pd.DataFrame:
    'Удаляется неинформативный ID'
    df = df.drop(['Loan_ID'], axis = 1)
    return df

class Custom_fillna_categories(BaseEstimator, TransformerMixin):
    'Заполнение категориальных столбцов модой'
    def __init__(self, mode_dict):
        self.mode_dict = mode_dict
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        X.fillna({'Gender': self.mode_dict['gender_mode']}, inplace=True)
        X.fillna({'Married': self.mode_dict['married_mode']}, inplace=True)
        X.fillna({'Dependents': self.mode_dict['dependents_mode']}, inplace=True)
        X.fillna({'Self_Employed': self.mode_dict['self_employed_mode']}, inplace=True)
        X.fillna({'Credit_History': self.mode_dict['credit_history_mode']}, inplace=True)
        X.fillna({'Loan_Amount_Term': self.mode_dict['loan_amount_term_mode']}, inplace=True)

        return X

class Custom_fillna_numerical(BaseEstimator, TransformerMixin):
    'Заполнение числовых столбцов медианой'
    def __init__(self, mean_dict):
        self.mean_dict = mean_dict
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        X.fillna({'LoanAmount': self.mean_dict['loan_amount_mean']}, inplace=True)

        return X


def encoder_categorical(df: pd.DataFrame) -> pd.DataFrame:
    'Кодирование категориальных признаков'
    df = pd.get_dummies(df)

    return df
    

def drop_after_dummies(df: pd.DataFrame) -> pd.DataFrame:
    'Удаление признаков'
    df = df.drop(['Gender_Female', 'Married_No', 'Education_Not Graduate', 
                'Self_Employed_No', 'Loan_Status_N'], axis = 1)
    return df

def rename_categorical(df: pd.DataFrame) -> pd.DataFrame:
    'Переименование признаков'
    new = {'Gender_Male': 'Gender', 'Married_Yes': 'Married', 
        'Education_Graduate': 'Education', 'Self_Employed_Yes': 'Self_Employed',
        'Loan_Status_Y': 'Loan_Status'}
    df.rename(columns=new, inplace=True)

    return df

def filter_outliers(df: pd.DataFrame) -> pd.DataFrame:
    'Устранение выбросов'
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]

    return df






def square_root_transform(df: pd.DataFrame) -> pd.DataFrame:
    'Преобразование квадратным корнем'
    df.ApplicantIncome = np.sqrt(df.ApplicantIncome)
    df.CoapplicantIncome = np.sqrt(df.CoapplicantIncome)
    df.LoanAmount = np.sqrt(df.LoanAmount)
    df = df.select_dtypes(exclude=['object', 'int64'])

    return df
import logging
import os
from datetime import datetime

modules_path = os.path.dirname(os.path.abspath(__file__))
print('FOLDER modules -> ', modules_path)

path = os.path.abspath(os.path.join(modules_path, "..", ".."))
print('FOLDER airflow_app -> ', path)

models_folder = path + '/data/models'
archive_folder = path + '/data/archive'

print('FOLDER models -> ', models_folder)
print('FOLDER archive -> ', archive_folder)

import dill
import json
import shutil
import random
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import FunctionTransformer
from sklearn.compose import ColumnTransformer
from imblearn.over_sampling import SMOTE
from sklearn.metrics import accuracy_score

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import CategoricalNB
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier

from sklearn.model_selection import GridSearchCV, RandomizedSearchCV

from .preprocessing_functions import drop_id, Custom_fillna_categories, Custom_fillna_numerical, \
    drop_after_dummies, rename_categorical, filter_outliers, square_root_transform
#
#
def checker() -> None:
    """ - Проверка существующей модели,
        - отправка её в архив с timestamp отметкой перемещения
        - запуск пайплайна c флагом train=True для обучения модели на текущих данных"""
    if not os.listdir(models_folder):
        go()
    else:
        log_event = 'Отправка старой модели в архив c timestamp события'
        logging.info(log_event)
        for m in os.listdir(models_folder):
            src_name = f'{models_folder}/{m}'
            dst_name = f'{models_folder}/{datetime.now().strftime("%Y%m%d%H%M")}_{m}'

            os.rename(src_name, dst_name)
            shutil.move(dst_name, archive_folder)

        go()


def get_predict() -> None:
    'Получить предсказание модели на актуальных тестовых данных'
    with open(f'{models_folder}/loan_predict.dill', 'rb') as file:
        model = dill.loads(file.read())

    log_event = f"{model['Meta']['Loan_ID'][0]}, {model['Meta']['Prediction']}"
    logging.info(log_event)


def go() -> None:
    """ - Пайплайн преобразования актуальных трейн/тест данных,
        - обучения 7 ML моделей и выбор лучшей из них,
        - предикт на тестовых данных и сохранение результата,
        - включающего в себя саму модель и метаданные с предиктом """

    print('Преобразование данных...')

    with open(f'{path}/data/test/test.json', 'r') as file:
        test_json_to_dict = json.loads(file.read())

    test_df = pd.DataFrame([test_json_to_dict])
    train_df = pd.read_csv(f'{path}/data/train/loan_data_set.csv')

    Loan_ID = test_df['Loan_ID']

    mode_dict = {
        'gender_mode': train_df['Gender'].mode()[0],
        'married_mode': train_df['Married'].mode()[0],
        'dependents_mode': train_df['Dependents'].mode()[0],
        'self_employed_mode': train_df['Self_Employed'].mode()[0],
        'credit_history_mode': train_df['Credit_History'].mode()[0],
        'loan_amount_term_mode': train_df['Loan_Amount_Term'].mode()[0]
    }

    mean_dict = {
        'loan_amount_mean': train_df['LoanAmount'].mean()
    }

    preprocessor1 = Pipeline(steps=[
        ('drop1', FunctionTransformer(drop_id)),
        ('fill_cats', Custom_fillna_categories(mode_dict)),
        ('fill_nums', Custom_fillna_numerical(mean_dict)),
    ])

    train_df = preprocessor1.fit_transform(train_df)
    test_df = preprocessor1.fit_transform(test_df)

    # Объединение train df и test df перед кодированием
    combined_df = pd.concat([train_df, test_df])
    # Кодирование категориальных признаков
    combined_df_encoded = pd.get_dummies(combined_df)
    # Разделение обратно на train df и test df
    train_df_encoded = combined_df_encoded.iloc[:len(train_df)]
    test_df_encoded = combined_df_encoded.iloc[len(train_df):]

    preprocessor2 = Pipeline(steps=[
        ('drop2', FunctionTransformer(drop_after_dummies)),
        ('rename', FunctionTransformer(rename_categorical)),
        ('outliers', FunctionTransformer(filter_outliers)),
        ('square_root', FunctionTransformer(square_root_transform)),
    ])

    train_df_encoded = preprocessor2.fit_transform(train_df_encoded)
    test_df_encoded = preprocessor2.fit_transform(test_df_encoded)

    # # Сохранение преобразованного тест датасета
    # test_df_encoded.to_csv(f'{path}/data/tmp/test_df.csv', index=False)

    X = train_df_encoded.drop(["Loan_Status"], axis=1)
    y = train_df_encoded["Loan_Status"]

    # ребалансировка для избежания oversampling
    X, y = SMOTE().fit_resample(X, y)
    # нормализация
    X_norm = MinMaxScaler().fit_transform(X)

    # разделение данных на обучающую и тестовую выборки
    X_train, X_test, y_train, y_test = train_test_split(X_norm, y, test_size=0.2, random_state=777)

    # Моделинг .......................................
    print('Моделинг...')

    print('\tЛогистическая регрессия...')
    LRclassifier = LogisticRegression(solver='saga', max_iter=500, random_state=777)
    LRclassifier.fit(X_train, y_train)
    y_pred = LRclassifier.predict(X_test)
    LRAcc = accuracy_score(y_pred, y_test)
    print('\t\t\t\t\t\tЗавершено')

    print('\tK-ближайших соседей классификатор...')
    scoreListknn = []
    KNclassifier = KNeighborsClassifier(1)
    for i in range(1, 21):
        KNclassifier = KNeighborsClassifier(n_neighbors=i)
        KNclassifier.fit(X_train, y_train)
        scoreListknn.append(KNclassifier.score(X_test, y_test))
    KNAcc = max(scoreListknn)
    print('\t\t\t\t\t\tЗавершено')

    print('\tМетод опорных векторов...')
    SVCclassifier = SVC(kernel='rbf', max_iter=500, random_state=777)
    SVCclassifier.fit(X_train, y_train)
    y_pred = SVCclassifier.predict(X_test)
    SVCAcc = accuracy_score(y_pred, y_test)
    print('\t\t\t\t\t\tЗавершено')

    print('\tНаивный Байес Гаусс классификатор...')
    NBclassifier2 = GaussianNB()
    NBclassifier2.fit(X_train, y_train)
    y_pred = NBclassifier2.predict(X_test)
    NBAcc2 = accuracy_score(y_pred, y_test)
    print('\t\t\t\t\t\tЗавершено')

    print('\tРешающее дерево...')
    scoreListDT = []
    DTclassifier = DecisionTreeClassifier(max_leaf_nodes=2, random_state=777)
    for i in range(2, 21):
        DTclassifier = DecisionTreeClassifier(max_leaf_nodes=i, random_state=777)
        DTclassifier.fit(X_train, y_train)
        scoreListDT.append(DTclassifier.score(X_test, y_test))
    DTAcc = max(scoreListDT)
    print('\t\t\t\t\t\tЗавершено')

    print('\tСлучайный лес...')
    scoreListRF = []
    RFclassifier = RandomForestClassifier(n_estimators=1000, random_state=777, max_leaf_nodes=2)
    for i in range(2, 25):
        RFclassifier = RandomForestClassifier(n_estimators=1000, random_state=777, max_leaf_nodes=i)
        RFclassifier.fit(X_train, y_train)
        scoreListRF.append(RFclassifier.score(X_test, y_test))
    RFAcc = max(scoreListRF)
    print('\t\t\t\t\t\tЗавершено')

    print('\tГрадиентный бустинг...')
    paramsGB = {'n_estimators': [100, 200, 300, 400, 500],
                'max_depth': [1, 2, 3, 4, 5],
                'subsample': [0.5, 1],
                'max_leaf_nodes': [2, 5, 10, 20, 30, 40, 50]}
    GB = RandomizedSearchCV(GradientBoostingClassifier(), paramsGB, cv=20)
    GB.fit(X_train, y_train)
    GBclassifier = GradientBoostingClassifier(subsample=0.5, n_estimators=400, max_depth=4, max_leaf_nodes=10,
                                              random_state=777)
    GBclassifier.fit(X_train, y_train)
    y_pred = GBclassifier.predict(X_test)
    GBAcc = accuracy_score(y_pred, y_test)
    print('\t\t\t\t\t\tЗавершено')
    # Отчет по моделям
    report = pd.DataFrame({'Model': [LRclassifier, KNclassifier, SVCclassifier,
                                     NBclassifier2, DTclassifier,
                                     RFclassifier, GBclassifier],
                           'Accuracy_train': [LRAcc * 100, KNAcc * 100, SVCAcc * 100,
                                              NBAcc2 * 100, DTAcc * 100,
                                              RFAcc * 100, GBAcc * 100]})
    report.sort_values(by='Accuracy_train', ascending=False)



    # -----------------------------------------------------------------------------

    # Нахождение лучшей модели на тестовых данных
    print('Выбор лучшей модели...')

    X_test = test_df_encoded.drop(["Loan_Status"], axis=1)
    y_test = test_df_encoded["Loan_Status"]

    models = report['Model'].to_list()
    accuracy_train = report['Accuracy_train'].to_list()
    delta = []
    accuracy_test = []

    for i, model in enumerate(models):
        y_pred = model.predict(X_test.values)
        acc_test = accuracy_score(y_test, y_pred)
        accuracy_test.append(acc_test)
        delta.append(abs(accuracy_train[i] - acc_test*100))

    min_delta = min(delta)
    min_delta_models = [model for model, d in zip(models, delta) if d == min_delta]

    best_model = random.choice(min_delta_models)
    best_model_name = type(best_model).__name__

    best_model_accuracy = None; best_model_prediction = None
    for model_name, acc, predict in zip(models, accuracy_train, accuracy_test):
        if model_name == best_model:
            best_model_accuracy = acc
            best_model_prediction = predict

    # Обучить на всех данных
    best_model.fit(X,y)

    print('Сохранение модели и метаданных...')
    # Сохранение параметров лучшей модели
    modeling_result = {
        'Model': best_model,
        'Meta': {
            'Accuracy_train': best_model_accuracy,
            'Prediction': best_model_prediction,
            'Loan_ID': Loan_ID,
            'Created': datetime.now().strftime("%Y-%m-%d %H:%M")
        }
    }

    # Запись модели и метаданных в файл
    with open(f'{path}/data/models/loan_predict.dill', 'wb') as f:
        dill.dump(modeling_result, f)

    print('\t\t\t\t\t\tЗавершено')

    # Логирование для Airflow
    train_predictions = [predict for predict in report['Accuracy_train'].values]
    avg_prediction = np.mean(train_predictions)

    log_event = f'Средний прогноз метрики accuracy на тестовых данных по 7 ML моделям: {avg_prediction:.3f}'
    logging.info(log_event)

    log_event = f'Модель {best_model_name} с самой большой точностью: {best_model_accuracy:.3f}'
    logging.info(log_event)

    get_predict()
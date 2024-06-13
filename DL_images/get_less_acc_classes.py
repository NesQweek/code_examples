import os
import pickle
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression

def get_classes(root_dir, filenames_path, feature_list_path, class_ids_path):
    # Загрузка файлов с характеристиками
    filenames = pickle.load(open(filenames_path, 'rb'))
    feature_list = pickle.load(open(feature_list_path, 'rb'))
    class_ids = pickle.load(open(class_ids_path, 'rb'))

    # Количество обучающих образцов, классов и размеры изображений
    TRAIN_SAMPLES = len(feature_list)
    NUM_CLASSES = 101

    # Загрузка меток классов
    class_names = sorted(os.listdir(root_dir))

    # Создание массивов для признаков и меток классов
    X = np.array(feature_list)
    y = np.zeros(TRAIN_SAMPLES)

    # Заполнение меток классов
    start = 0
    for i, class_name in enumerate(class_names):
        class_dir = os.path.join(root_dir, class_name)
        num_files = len(os.listdir(class_dir))
        y[start:start+num_files] = i
        start += num_files

    # Разделение данных на обучающую и тестовую выборки
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Обучение логистической регрессии
    clf = LogisticRegression(multi_class='multinomial', solver='lbfgs', max_iter=1000)
    clf.fit(X_train, y_train)

    # Предсказание и вычисление точности классификации
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Общая точность классификации: {accuracy*100:.2f}%")

    # Точность классификации для каждого класса
    class_accuracies = {}
    for i in range(NUM_CLASSES):
        class_mask = (y_test == i)
        class_y_test = y_test[class_mask]
        class_y_pred = y_pred[class_mask]
        class_accuracy = accuracy_score(class_y_test, class_y_pred)
        class_accuracies[class_names[i]] = class_accuracy * 100

    less_accurate_class = {}
    # Вывод точности классификации для каждого класса
    for class_name, accuracy in sorted(class_accuracies.items(), key=lambda x: x[1], reverse=True):
        if accuracy < 100:
            print(f"\t{class_name}: {accuracy:.2f}%")
            less_accurate_class[class_name] = accuracy

    return less_accurate_class
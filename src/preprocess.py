"""
Предобработка данных для кредитного скоринга.
Датасет: Default of Credit Card Clients (UCI).
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
import os

# Пути
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'credit_data.xls')
MODELS_DIR = os.path.join(BASE_DIR, 'models')


def load_data():
    """Загружает датасет и приводит названия колонок к удобному виду."""
    df = pd.read_excel(DATA_PATH, header=1)
    df = df.rename(columns={'default payment next month': 'target'})
    df = df.drop(columns=['ID'])
    return df


def prepare_data(test_size=0.3, random_state=42):
    """Разделяет данные, масштабирует признаки, сохраняет скейлер."""
    df = load_data()

    X = df.drop(columns=['target'])
    y = df['target']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Сохраняем скейлер и список колонок — понадобятся в веб-сервисе
    os.makedirs(MODELS_DIR, exist_ok=True)
    joblib.dump(scaler, os.path.join(MODELS_DIR, 'scaler.pkl'))
    joblib.dump(list(X.columns), os.path.join(MODELS_DIR, 'columns.pkl'))

    return X_train_scaled, X_test_scaled, y_train, y_test, X.columns


if __name__ == '__main__':
    X_train, X_test, y_train, y_test, cols = prepare_data()
    print("Обучающая выборка:", X_train.shape)
    print("Тестовая выборка:", X_test.shape)
    print("Признаки:", list(cols))
    print("Доля дефолтов в трейне:", y_train.mean().round(3))
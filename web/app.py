"""
Flask-приложение для кредитного скоринга.
Загружает обученную модель и делает предсказания по данным из формы.
Датасет: Default of Credit Card Clients (UCI).
"""
import os
import joblib
import numpy as np
from flask import Flask, request, render_template

# ---------- Пути ----------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, 'models')

# ---------- Flask ----------
app = Flask(__name__)

# ---------- Загрузка модели, скейлера и списка колонок ----------
model = joblib.load(os.path.join(MODELS_DIR, 'model.pkl'))
scaler = joblib.load(os.path.join(MODELS_DIR, 'scaler.pkl'))
columns = joblib.load(os.path.join(MODELS_DIR, 'columns.pkl'))


def proba_to_score(proba, min_score=300, max_score=850):
    """Переводит вероятность дефолта в скоринговый балл 300–850."""
    return int((1 - proba) * (max_score - min_score) + min_score)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    try:
        features = []

        # 1. Основные данные
        features.append(float(request.form['LIMIT_BAL']))
        features.append(float(request.form['SEX']))
        features.append(float(request.form['EDUCATION']))
        features.append(float(request.form['MARRIAGE']))
        features.append(float(request.form['AGE']))

        # 2. История просрочек: PAY_0, PAY_2 … PAY_6
        features.append(float(request.form['PAY_0']))
        for i in range(2, 7):
            features.append(float(request.form[f'PAY_{i}']))

        # 3. Суммы по счетам
        for i in range(1, 7):
            features.append(float(request.form[f'BILL_AMT{i}']))

        # 4. Фактические платежи
        for i in range(1, 7):
            features.append(float(request.form[f'PAY_AMT{i}']))

        if len(features) != 23:
            raise ValueError(f"Ожидалось 23 признака, получено {len(features)}")

        X = np.array([features])
        X_scaled = scaler.transform(X)
        proba = model.predict_proba(X_scaled)[0, 1]
        score = proba_to_score(proba)

        if score >= 700:
            decision, color = "Одобрить", "green"
        elif score >= 600:
            decision, color = "Одобрить с осторожностью", "orange"
        else:
            decision, color = "Отказать", "red"

        return render_template(
            'index.html',
            prediction_text=f"Вероятность дефолта: {proba:.2%}",
            score_text=f"Скоринговый балл: {score}",
            decision_text=f"Решение: {decision}",
            color=color,
            form_data=request.form
        )
    except Exception as e:
        return render_template(
            'index.html',
            error=f"Ошибка: {e}",
            form_data=request.form
        )


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
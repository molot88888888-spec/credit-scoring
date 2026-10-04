# Credit Scoring — оценка кредитного риска

Мини-проект по теме 8: построение скоринговой модели для предсказания
вероятности дефолта заёмщика.

## Данные
Default of Credit Card Clients (UCI):
https://archive.ics.uci.edu/ml/datasets/default+of+credit+card+clients

30 000 клиентов, 23 признака, дисбаланс классов ~22%.

## Структура проекта
credit-scoring/
├── data/ # датасет (скачивается отдельно)
├── notebooks/ # разведочный анализ
├── src/
│ ├── preprocess.py # загрузка и предобработка
│ └── train.py # обучение моделей
├── models/ # сохранённые модель, скейлер, колонки
├── web/
│ ├── app.py # Flask-сервис
│ └── templates/
│ └── index.html # HTML-форма
└── requirements.txt

## Модели и метрики
| Модель | Accuracy | Precision | Recall | F1 | ROC-AUC |
|--------|----------|-----------|--------|-----|---------|
| LogisticRegression | 0.684 | 0.373 | 0.628 | 0.468 | 0.716 |
| DecisionTree | 0.781 | 0.505 | 0.540 | 0.522 | 0.756 |
| RandomForest | 0.802 | 0.561 | 0.483 | 0.519 | 0.762 |
| GradientBoosting | 0.816 | 0.657 | 0.357 | 0.463 | 0.780 |

## Запуск

```bash
# 1. Клонировать репозиторий
git clone https://github.com/USERNAME/credit-scoring.git
cd credit-scoring

# 2. Создать виртуальное окружение
python -m venv venv
venv\Scripts\activate     # Windows
# source venv/bin/activate  # Linux/Mac

# 3. Установить зависимости
pip install -r requirements.txt

# 4. Скачать датасет в data/
# https://archive.ics.uci.edu/ml/machine-learning-databases/00350/default%20of%20credit%20card%20clients.xls
# Сохранить как data/credit_data.xls

# 5. Обучить модель
cd src
python preprocess.py
python train.py

# 6. Запустить веб-сервис
cd ../web
python app.py
Открыть http://127.0.0.1:5000
Выводы
Дисбаланс классов требует использования recall, F1, ROC-AUC, а не accuracy.

GradientBoosting точнее, но пропускает больше дефолтов.

LogisticRegression интерпретируема — предпочтительна для регуляторных требований.

Демографические признаки (SEX, MARRIAGE, EDUCATION) почти не влияют на прогноз.

Ограничения
Один датасет (Тайвань, 2005).

Нет внешних данных (кредитная история, макроэкономика).

Модель не учитывает временную динамику.

# Credit Scoring — оценка кредитного риска

Мини-проект по теме 8: построение скоринговой модели для предсказания
вероятности дефолта заёмщика.

## Данные
Default of Credit Card Clients (UCI):
https://archive.ics.uci.edu/ml/datasets/default+of+credit+card+clients

30 000 клиентов, 23 признака, дисбаланс классов ~22%.

## Структура
- `data/` — исходные данные
- `notebooks/` — разведочный анализ (Jupyter)
- `src/preprocess.py` — загрузка и предобработка
- `src/train.py` — обучение 4 моделей
- `models/` — сохранённые модель, скейлер, список колонок
- `web/` — Flask-сервис с HTML-формой

## Модели
| Модель | ROC-AUC | Recall |
|--------|---------|--------|
| LogisticRegression | 0.716 | 0.628 |
| DecisionTree | 0.756 | 0.540 |
| RandomForest | 0.762 | 0.483 |
| GradientBoosting | 0.780 | 0.357 |

Лучшая по ROC-AUC: GradientBoosting.
Лучшая по recall: LogisticRegression (важно для скоринга).

## Запуск
```bash
pip install -r requirements.txt
cd src && python preprocess.py
cd src && python train.py
cd web && python app.py
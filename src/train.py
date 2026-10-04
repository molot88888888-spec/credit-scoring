"""
Обучение моделей кредитного скоринга.
Сравнивает 4 модели, сохраняет лучшую в models/model.pkl.
"""
import os
import joblib
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, roc_auc_score, confusion_matrix,
                             roc_curve)

from preprocess import prepare_data, MODELS_DIR


def train_models():
    X_train, X_test, y_train, y_test, cols = prepare_data()

    models = {
        'LogisticRegression': LogisticRegression(
            class_weight='balanced', max_iter=1000, random_state=42
        ),
        'DecisionTree': DecisionTreeClassifier(
            class_weight='balanced', max_depth=5, random_state=42
        ),
        'RandomForest': RandomForestClassifier(
            class_weight='balanced', n_estimators=200, random_state=42, n_jobs=-1
        ),
        'GradientBoosting': GradientBoostingClassifier(
            n_estimators=200, random_state=42
        ),
    }

    results = {}
    for name, model in models.items():
        print(f"\nОбучение {name}...")
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        y_proba = model.predict_proba(X_test)[:, 1]

        results[name] = {
            'model': model,
            'Accuracy':  accuracy_score(y_test, y_pred),
            'Precision': precision_score(y_test, y_pred),
            'Recall':    recall_score(y_test, y_pred),
            'F1':        f1_score(y_test, y_pred),
            'ROC-AUC':   roc_auc_score(y_test, y_proba),
            'y_proba':   y_proba,
            'y_pred':    y_pred,
        }

    # Таблица метрик
    metrics_df = pd.DataFrame({
        k: {m: v for m, v in r.items() if m not in ('model', 'y_proba', 'y_pred')}
        for k, r in results.items()
    }).T
    print("\n=== Метрики ===")
    print(metrics_df.round(3))

    # Сохраняем лучшую модель по ROC-AUC
    best_name = metrics_df['ROC-AUC'].idxmax()
    best_model = results[best_name]['model']
    joblib.dump(best_model, os.path.join(MODELS_DIR, 'model.pkl'))
    print(f"\nЛучшая модель: {best_name} (ROC-AUC = {metrics_df.loc[best_name, 'ROC-AUC']:.3f})")
    print(f"Сохранена в models/model.pkl")

    # ROC-кривые
    plt.figure(figsize=(8, 6))
    for name, r in results.items():
        fpr, tpr, _ = roc_curve(y_test, r['y_proba'])
        plt.plot(fpr, tpr, label=f"{name} (AUC = {r['ROC-AUC']:.3f})")
    plt.plot([0, 1], [0, 1], 'k--', label='Случайная')
    plt.xlabel('FPR')
    plt.ylabel('TPR')
    plt.title('ROC-кривые')
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(MODELS_DIR, '..', 'roc_curves.png'), dpi=100)
    plt.show()

    return results


if __name__ == '__main__':
    train_models()
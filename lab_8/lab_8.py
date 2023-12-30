import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from pyod.models.knn import KNN
import seaborn as sns

# Оцінка суми кредиту
def evaluate_loan_amount(loan_amount):
    if loan_amount < 1000:
        return 4
    elif 1000 <= loan_amount < 5000:
        return 3
    elif 5000 <= loan_amount < 10000:
        return 2
    else:
        return 1

# Оцінка терміну погашення кредиту
def evaluate_loan_days(loan_days):
    if loan_days < 7:
        return 4
    elif 7 <= loan_days < 30:
        return 3
    elif 30 <= loan_days < 90:
        return 2
    else:
        return 1

# Оцінка статі
def evaluate_gender(gender_id):
    if gender_id == 1:
        return 2
    else:
        return 1

# Оцінка кількості дітей
def evaluate_children_count(children_count_id):
    if children_count_id == 0:
        return 1
    elif 1 <= children_count_id < 2:
        return 2
    elif 3 <= children_count_id < 4:
        return 3
    else:
        return 4

# Оцінка рівня освіти
def evaluate_education(education_id):
    if education_id == 1:
        return 1
    elif 2 <= education_id < 3:
        return 2
    elif 4 <= education_id < 5:
        return 3
    else:
        return 4

# Оцінка наявності нерухомості
def evaluate_immovables(has_immovables):
    if has_immovables == 1:
        return 3
    else:
        return 1

# Оцінка навяності транспортного засобу
def evaluate_movables(has_movables):
    if has_movables == 1:
        return 2
    else:
        return 1

# Оцінка типу зайнятості
def evaluate_employment_type(employment_type_id):
    if employment_type_id == 1:
        return 1
    elif 2 <= employment_type_id < 3:
        return 2
    elif 4 <= employment_type_id < 5:
        return 3
    else:
        return 4

# Оцінка щомісячних доходів
def evaluate_monthly_income(monthly_income):
    if monthly_income < 5000:
        return 1
    elif 5000 <= monthly_income < 10000:
        return 2
    elif 10000 <= monthly_income < 20000:
        return 3
    elif 20000 <= monthly_income < 40000:
        return 4
    else:
        return 5

# Оцінка щомісячних витрат
def evaluate_monthly_expenses(monthly_expenses):
    if monthly_expenses < 5000:
        return 5
    elif 5000 <= monthly_expenses < 10000:
        return 4
    elif 10000 <= monthly_expenses < 20000:
        return 3
    elif 20000 <= monthly_expenses < 40000:
        return 2
    else:
        return 1

# Оцінка присутніх погашених позик
def evaluate_other_loans_has_closed(other_loans_has_closed):
    if other_loans_has_closed == 1:
        return 2
    else:
        return -2

# Оцінка присутніх непогашених позик
def evaluate_other_loans_active(other_loans_active):
    if other_loans_active == 1:
        return -2
    else:
        return 1

# Оцінка загального розміру непогашених позиків
def evaluate_other_loans_about_current(other_loans_about_current):
    if other_loans_about_current == 0:
        return 3
    elif 1 <= other_loans_about_current < 5000:
        return -1
    elif 5000 <= other_loans_about_current < 10000:
        return -2
    else:
        return -3

# Функція нарахування балів по кожному параметру
def calculate_score(data):
    # Ваги для кожного показника
    weights = {
        'loan_amount': 0.05,
        'loan_days': 0.03,
        'gender_id': 0.06,
        'children_count_id': 0.05,
        'education_id': 0.05,
        'has_immovables': 0.04,
        'has_movables': 0.02,
        'employment_type_id': 0.08,
        'monthly_income': 0.07,
        'monthly_expenses': 0.06,
        'other_loans_has_closed': 0.05,
        'other_loans_active': 0.05,
        'other_loans_about_current': 0.04,
    }

    # Обчислення балів для кожного показника
    total_score = 0
    intermediate_scores = {}

    for param, value in data.items():
        if param in weights:
            if param == 'loan_amount':
                param_score = evaluate_loan_amount(value)
            elif param == 'loan_days':
                param_score = evaluate_loan_days(value)
            elif param == 'gender_id':
                param_score = evaluate_gender(value)
            elif param == 'children_count_id':
                param_score = evaluate_children_count(value)
            elif param == 'education_id':
                param_score = evaluate_education(value)
            elif param == 'has_immovables':
                param_score = evaluate_immovables(value)
            elif param == 'has_movables':
                param_score = evaluate_movables(value)
            elif param == 'employment_type_id':
                param_score = evaluate_employment_type(value)
            elif param == 'monthly_income':
                param_score = evaluate_monthly_income(value)
            elif param == 'monthly_expenses':
                param_score = evaluate_monthly_expenses(value)
            elif param == 'other_loans_has_closed':
                param_score = evaluate_other_loans_has_closed(value)
            elif param == 'other_loans_active':
                param_score = evaluate_other_loans_active(value)
            elif param == 'other_loans_about_current':
                param_score = evaluate_other_loans_about_current(value)

            intermediate_scores[param] = param_score * weights[param]  # Зберегти проміжний бал з урахуванням ваги
            total_score += intermediate_scores[param]

    intermediate_scores['Total_Score'] = total_score
    intermediate_scores['Decision'] = decide_loan_approval(total_score)

    return intermediate_scores

# Функція для прийняття рішення щодо видачі кредиту чи відмови
def decide_loan_approval(total_score):
    if total_score >= 1.2:
        return "Approved"
    else:
        return "Denied"

# Функція для виявлення шахрайства
def fraud_detection(X):
    outliers_fraction = 0.1
    clf = KNN(contamination=outliers_fraction)
    clf.fit(X)
    y_pred = clf.predict(X)
    return y_pred

# Функція для відображення графіка шахрайства
def plot_fraud_detection(X, y_pred):
    norm_data = StandardScaler().fit_transform(X)
    compressed = PCA(n_components=2).fit_transform(norm_data)
    plt.figure(figsize=(10, 5))
    sns.scatterplot(x=compressed[:, 0], y=compressed[:, 1], hue=np.where(y_pred, "fraud", "no fraud"))
    plt.show()

# Функція для підрахунку відсотків шахрайства
def calculate_fraud_percentages(y_pred):
    fraud_percentage = (y_pred.sum() / len(y_pred)) * 100
    no_fraud_percentage = 100 - fraud_percentage
    return fraud_percentage, no_fraud_percentage

def credit():
    # Обчислення балів та рішення для кожного клієнта
    results = []
    for index, row in df.iterrows():
        input_data = row.to_dict()
        intermediate_scores = calculate_score(input_data)
        # Зберегти результати
        results.append(intermediate_scores)

    # Виведення та збереження результатів
    result_df = pd.DataFrame(results)
    result_df.to_excel('final_results.xlsx', index=False)
    print(result_df)

    # Розрахунок та відображення відсотків
    approval_percentage = (result_df['Decision'].value_counts()['Approved'] / len(result_df)) * 100
    denial_percentage = 100 - approval_percentage
    print(f'\nВідсоток клієнтів, яким надали кредит: {approval_percentage:.2f}%')
    print(f'Відсоток клієнтів, яким відмовлено в кредиті: {denial_percentage:.2f}%\n')

    # Відображення scatter графіку
    plt.scatter(result_df['Total_Score'], result_df.index,
                c=result_df['Decision'].apply(lambda x: 1 if x == 'Approved' else 0), cmap='viridis')
    plt.title('Scatter графік результатів класифікації')
    plt.xlabel('Total Score')
    plt.ylabel('Клієнт')
    plt.colorbar(ticks=[0, 1], label='Рішення: 0 - Відмова, 1 - Затверджено')
    plt.show()

    return result_df

def fraud(result_df):
    X = result_df.drop(['Total_Score', 'Decision'], axis=1)  # Виключаємо колонки з результатами
    y_pred_fraud = fraud_detection(X)

    # Додаємо колонку з предсказаною міткою шахрайства в результати
    result_df['Fraud_Prediction'] = y_pred_fraud

    # Вивід результатів
    print(result_df)

    # Підрахунок та відображення відсотків шахрайства
    fraud_percentage, no_fraud_percentage = calculate_fraud_percentages(y_pred_fraud)
    print(f'\nВідсоток клієнтів, які виявлені як шахраї: {fraud_percentage:.2f}%')
    print(f'Відсоток клієнтів, які не виявлені як шахраї: {no_fraud_percentage:.2f}%\n')

    # Відображення scatter графіку для виявлення шахрайства
    plot_fraud_detection(X, y_pred_fraud)

    return

# Головні виклики
if __name__ == '__main__':
    # Завантаження даних
    df = pd.read_excel('dataset/d_segment_sample_cleaning.xlsx')

    #  Прийняття рішення про надання кредиту
    result_df = credit()

    # Детекція шахрайства
    fraud(result_df)
import pandas as pd
from sklearn.preprocessing import StandardScaler
from keras import models
from keras import layers
from keras.models import Model, Sequential
from keras.layers import Input, Dense, LSTM, Conv1D, MaxPooling1D, Flatten
import matplotlib.pyplot as plt
import numpy as np

# Усунення warning
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Завантаження даних
def data_load():
    x_train = pd.read_csv(r'dataset/train_dataset.csv')
    y_train = pd.read_csv(r'dataset/train_mark.csv')
    x_test = pd.read_csv(r'dataset/test_dataset.csv')
    y_test = pd.read_csv(r'dataset/test_mark.csv')

    return x_train, y_train, x_test, y_test

# Первинна обробка даних
def data_procesing(x_train, x_test, y_train, y_test):
    # Видалення стовпця з іменами
    x_train = x_train.iloc[:, 1:]
    x_test = x_test.iloc[:, 1:]
    # Перетворення рядкових значень на числові
    y_train = y_train.replace({'зараховано': 0, 'незараховано': 1}).to_numpy()
    y_test = y_test.replace({'зараховано': 0, 'незараховано': 1}).to_numpy()
    # Перетворення типу даних
    x_train = x_train.astype('float32').to_numpy()
    x_test = x_test.astype('float32').to_numpy()

    return x_train, y_train, x_test, y_test

# Нормалізація даних
def normalize_data(x_train, x_test):
    scaler = StandardScaler()
    x_train = scaler.fit_transform(x_train)
    x_test = scaler.transform(x_test)

    return x_train, x_test

# Архітектура моделі
def network_architecture(data_mode):
    # Архітектура - Sequential
    if (data_mode == 1):
        network = models.Sequential()
        network.add(layers.Dense(16, activation='relu', input_dim=5))
        network.add(layers.Dense(8, activation='relu'))
        network.add(layers.Dense(1, activation='sigmoid'))
    # Архітектура - Functional
    elif (data_mode == 2):
        input_layer = Input(shape=(5,))
        hidden_layer1 = Dense(16, activation='relu')(input_layer)
        hidden_layer2 = Dense(8, activation='relu')(hidden_layer1)
        output_layer = Dense(1, activation='sigmoid')(hidden_layer2)
        network = Model(inputs=input_layer, outputs=output_layer)
    # Архітектура - CNN
    elif (data_mode == 3):
        network = Sequential()
        network.add(Conv1D(32, 2, activation='relu', input_shape=(x_train.shape[1], 1)))
        network.add(MaxPooling1D(1))
        network.add(Conv1D(64, 2, activation='relu'))
        network.add(Flatten())
        network.add(Dense(64, activation='relu'))
        network.add(Dense(1, activation='sigmoid'))
    # Архітектура - RNN
    else:
        network = Sequential()
        network.add(LSTM(32, activation='relu', input_shape=(x_train.shape[1], 1)))
        network.add(Dense(1, activation='sigmoid'))
    print('\nАрхітектура моделі')
    network.summary()

    return network

# Компіляція та навчання мережі
def compile_train(network, x_train, y_train, x_test, y_test):
    network.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    print('\nНавчання моделі')

    epochs = 10
    batch_size = 32

    mse_train_values = []  # Зберігатиме значення MSE для тренування
    mse_test_values = []   # Зберігатиме значення MSE для тестування
    iterations = []        # Зберігатиме номери ітерацій

    for epoch in range(epochs):
        # Навчання моделі протягом кожної епохи
        history = network.fit(x_train, y_train, epochs=1, batch_size=batch_size, verbose=0)

        # Отримання значення MSE для тренування та тестування
        mse_train = history.history['loss'][0]
        mse_test = network.evaluate(x_test, y_test, verbose=0)[0]

        # Зберігання значень MSE та номерів ітерацій
        mse_train_values.append(mse_train)
        mse_test_values.append(mse_test)
        iterations.append(epoch)

        # Відображення інформації про поточну епоху
        print(f'Epoch {epoch + 1}/{epochs},\tТренувальна MSE: {mse_train},\tТестова MSE: {mse_test}')

        # Відображення графіка навчання та прогнозування
        pred = network.predict(x_test)
        plt.plot(y_test, label='Реальні')
        plt.plot(pred, label='Прогнозовані')
        plt.title(f'Епоха {epoch + 1}')
        plt.xlabel('Кількість абітурінтів')
        plt.ylabel('Рішення')
        plt.legend()
        plt.show()

    # Відображення графіків
    plt.plot(iterations, mse_train_values, label='Тренувальна MSE')
    plt.plot(iterations, mse_test_values, label='Тестова MSE')
    plt.title('Динаміка навчання')
    plt.xlabel('Епохи')
    plt.ylabel('MSE')
    plt.legend()
    plt.show()

    return network

# Перевірка моделі
def test(network, data_mode):
    print('\nПеревірка моделі')
    predicted_probabilities = network.predict(x_test)
    predicted_classes = (predicted_probabilities > 0.5).astype(int)
    test_results = pd.DataFrame({'Predicted': predicted_classes.flatten(), 'Actual': y_test.flatten()})
    test_loss, test_acc = network.evaluate(x_test, y_test)

    # Збереження результатів у таблицю
    test_results.to_excel('model_{0}.xlsx'.format(data_mode), index=False)

    # Графік для оцінки точності
    plt.figure(figsize=(12, 6))
    # Перший графік
    plt.subplot(1, 2, 1)
    plt.plot(test_results.index, test_results['Predicted'], label='Прогнозовані', marker='x', linestyle='None', color='r')
    plt.plot(test_results.index, test_results['Actual'], label='Реальні', marker='o', linestyle='None', color='b')
    plt.xlabel('Кількість абітурієнтів')
    plt.ylabel('Рішення')
    plt.legend()
    # Другий графік
    plt.subplot(1, 2, 2)
    plt.scatter(np.arange(len(y_test)), y_test, label='Реальні', marker='o', color='b')
    plt.scatter(np.arange(len(predicted_classes)), predicted_classes, label='Прогнозовані', marker='x', color='r')
    plt.xlabel('Кількість абітурієнтів')
    plt.ylabel('Рішення')
    plt.legend()
    # Відображення графіків
    plt.suptitle('Порівняння реальних та прогнозованих даних')
    plt.tight_layout()
    plt.show()

    return

# Головні виклики

descriptions = ['Sequential', 'Functional', 'CNN', 'RNN']

# Вибір режиму роботи програми
print('Оберіть тип нейронної мережі:')
for i in range(len(descriptions)):
    print(i + 1, '-', descriptions[i])
data_mode = int(input('mode:'))
# Якщо джерело даних існує
if data_mode in range(1, len(descriptions) + 1):

    # Завантаження даних
    x_train, y_train, x_test, y_test = data_load()

    # Первинна обробка даних
    x_train, y_train, x_test, y_test = data_procesing(x_train, x_test, y_train, y_test)

    # Нормалізація даних
    x_train, x_test = normalize_data(x_train, x_test)

    # Архітектура мережі
    network = network_architecture(data_mode)

    # Компіляція та навчання мережі
    network = compile_train(network, x_train, y_train, x_test, y_test)

    # Перевірка мережі
    test(network, data_mode)
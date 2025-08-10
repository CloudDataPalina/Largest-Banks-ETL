# Импорт библиотеки pandas для работы с таблицами
import pandas as pd

# Определяем функцию-тест для проверки работы функции transform()
def test_transform():
    '''
    Тест проверяет корректность функции transform() 
    при использовании тестового DataFrame и фиктивных валютных курсов.
    '''

    # Создаём тестовый DataFrame с двумя банками и их рыночной капитализацией в миллиардах USD
    test_df = pd.DataFrame({
        'Name': ['Bank A', 'Bank B'],
        'MC_USD_Billion': [100, 200]                # рыночная капитализация в долларах
    })

    # Задаём фиктивные курсы валют (как будто они прочитаны из CSV-файла)
    test_exchange = {
        'EUR': 0.9,                                # курс EUR к USD
        'GBP': 0.8,                                # курс GBP к USD
        'INR': 83.0                                # курс индийской рупии к USD
    }

    # Эмуляция работы функции transform() — преобразуем данные
    def transform_test(df):
        # Добавляем столбец с капитализацией в EUR
        df['MC_EUR_Billion'] = df['MC_USD_Billion'] * test_exchange['EUR']       # Добавляем столбец с капитализацией в GBP
        df['MC_GBP_Billion'] = df['MC_USD_Billion'] * test_exchange['GBP']       # Добавляем столбец с капитализацией в INR
        df['MC_INR_Billion'] = df['MC_USD_Billion'] * test_exchange['INR']       # Округляем все числовые значения до двух знаков после запятой
        df = df.round(2)
        return df

    # Вызываем трансформацию и получаем результат
    result_df = transform_test(test_df)

    # Проверяем правильность расчётов через утверждения (assert)
    assert result_df.loc[0, 'MC_EUR_Billion'] == 90.00                 # 100 USD × 0.9 = 90.00
    assert result_df.loc[1, 'MC_GBP_Billion'] == 160.00                # 200 USD × 0.8 = 160.00 
    assert result_df.loc[0, 'MC_INR_Billion'] == 8300.00               # 100 USD × 83 = 8300.00

    # Если все assert'ы прошли — выводим сообщение
    print(" Тест пройден успешно.")

# Этот блок выполняется только если запустить файл напрямую
if __name__ == "__main__":
    test_transform()                                 # Запускаем тест

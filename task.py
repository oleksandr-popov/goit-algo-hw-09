import timeit

# Визначаємо доступні номінали монет
denominations = [50, 25, 10, 5, 2, 1]


def find_coins_greedy(amount):
    """
    Знаходить кількість монет, використовуючи простий жадібний підхід.
    Алгоритм бере якомога більше найбільших монет, а потім переходить до наступних за розміром.
    """
    coin_counts = {}
    remaining_amount = amount

    # Ітеруємо через номінали від найбільшого до найменшого
    for coin in denominations:
        if remaining_amount >= coin:
            # Обчислюємо, скільки поточних монет можна використати
            count = remaining_amount // coin
            coin_counts[coin] = count

            # Оновлюємо суму, що залишилася
            remaining_amount %= coin

    return coin_counts


def find_min_coins(amount):
    """
    Знаходить мінімальну кількість монет для заданої суми, використовуючи Динамічне Програмування.
    Рішення будується поступово, починаючи з 1 і до цільової суми.
    """

    # min_coins[x] зберігає мінімальну кількість монет, необхідну для отримання суми x
    # Ми використовуємо розмір 'amount + 1', оскільки індексуємо від 0 до 'amount'.
    min_coins = [0] + [float("inf")] * amount

    # coin_count[x] зберігає фактичний словник монет, використаних для отримання суми x
    coin_count = [{} for _ in range(amount + 1)]

    # Ітеруємо через кожен номінал монети
    for coin in denominations:
        # Ітеруємо через усі суми від значення монети до цільової суми
        for x in range(coin, amount + 1):

            # Якщо використання поточної монети дає меншу загальну кількість монет, ніж поточний мінімум
            if min_coins[x - coin] + 1 < min_coins[x]:
                # Оновлюємо мінімальну кількість монет для суми x
                min_coins[x] = min_coins[x - coin] + 1

                # Оновлюємо фактичний склад монет для суми x
                # Копіюємо склад монет для залишку (x - coin)
                coin_count[x] = coin_count[x - coin].copy()

                # Збільшуємо лічильник поточної монети
                coin_count[x][coin] = coin_count[x].get(coin, 0) + 1
    return coin_count[amount]


if __name__ == "__main__":
    # Суми для тестування
    amounts_to_test = [10, 55, 113, 207, 505, 1001]
    results = []

    # Кількість разів для запуску кожної функції для точного вимірювання часу
    NUM_RUNS = 1000

    for amount in amounts_to_test:
        # Вимірюємо час виконання жадібної функції
        time_greedy = timeit.timeit(lambda: find_coins_greedy(amount), number=NUM_RUNS)

        # Вимірюємо час виконання функції Динамічного Програмування
        time_dp = timeit.timeit(lambda: find_min_coins(amount), number=NUM_RUNS)

        results.append([amount, time_greedy, time_dp])

    # Виводимо результати у відформатованій таблиці
    print("\nПорівняння продуктивності (1000 запусків):")
    print("-" * 43)
    print("  Сума  | Час Жадібний (с) | Час ДП (с)")
    print("-" * 43)
    for result in results:
        print(f"{result[0]:>6} | {result[1]:>15.8f}   |   {result[2]:>10.8f}")
    print("-" * 43)

    # Приклад різниці у виводі для однієї суми
    sample_amount = amounts_to_test[-1]
    print(f"\nСклад Монет для Суми {sample_amount}:")
    print(f"  Результат Жадібного:                   {find_coins_greedy(sample_amount)}")
    print(f"  Результат Динам.Программування:        {find_min_coins(sample_amount)}")

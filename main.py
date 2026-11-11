"""ЛР № 8, вариант 13. Размен суммы: номиналы 1, 5, 11; S <= 120.
Критерий 1 - наибольший номинал, критерий 2 - наименьший, Ж6 - улучшенная схема."""
import random      # генерация случайных сумм
import statistics  # среднее и медиана
import time        # замер времени работы

COINS = [1, 5, 11]  # система номиналов варианта
S_MAX = 120         # максимальная размениваемая сумма


def coins_dp(s, coins):
    """Точный алгоритм (ДП): минимальное число монет для суммы s."""
    d = [0] * (s + 1)                                   # d[x] - минимум монет для суммы x; d[0] = 0
    for x in range(1, s + 1):                           # перебираем все суммы от 1 до s
        d[x] = min(d[x - c] for c in coins if c <= x) + 1  # последняя монета c: берём лучший вариант
    return d[s]                                         # ответ для исходной суммы


def greedy(s, coins, largest=True):
    """Жадный размен: largest=True - наибольший номинал, False - наименьший."""
    count = 0                                           # счётчик монет
    for c in sorted(coins, reverse=largest):            # порядок номиналов задаёт критерий выбора
        count += s // c                                 # берём монету c максимально возможное число раз
        s %= c                                          # остаток суммы после этого
    return count                                        # число использованных монет


def greedy_improved(s, coins):
    """Ж6: перебор первой монеты (локальное улучшение), дальше - жадно по наибольшему."""
    return min(1 + greedy(s - c, coins) for c in coins if c <= s)  # лучшая первая монета + жадный хвост


def best_of_two(s, coins):
    """Ж6: лучшее из результатов двух критериев."""
    return min(greedy(s, coins, True), greedy(s, coins, False))    # меньшее из двух чисел монет


def evaluate(name, func, sums):
    """Отклонение func от оптимума на списке сумм; печатает строку таблицы."""
    dev, hits = [], 0                                   # отклонения и число точных совпадений
    for s in sums:                                      # проходим по всем наборам данных
        opt, got = coins_dp(s, COINS), func(s, COINS)   # эталон и проверяемый алгоритм
        dev.append((got - opt) / opt * 100)             # относительное отклонение, % (минимизация)
        hits += got == opt                              # считаем совпадения с оптимумом
    print(f"{name:<28}{statistics.mean(dev):>10.2f}{statistics.median(dev):>10.2f}"
          f"{max(dev):>10.2f}{hits / len(sums) * 100:>10.1f}%")  # среднее, медиана, максимум, доля


if __name__ == "__main__":
    # --- Контрпример: наименьшая сумма, на которой жадный (наибольший) неоптимален ---
    s0 = next(s for s in range(1, S_MAX + 1) if greedy(s, COINS) != coins_dp(s, COINS))  # поиск
    print(f"Контрпример: S = {s0}, жадно {greedy(s0, COINS)} монет, оптимум {coins_dp(s0, COINS)}")
    bad = [s for s in range(1, S_MAX + 1) if greedy(s, COINS) != coins_dp(s, COINS)]     # все плохие S
    print(f"Сумм, где жадный неоптимален: {len(bad)} из {S_MAX}\n")

    # --- Серия из 500 случайных сумм и полный перебор S = 1..120 ---
    rng = random.Random(2024)                           # фиксированное зерно - результат повторяем
    sets = {"500 случайных S": [rng.randint(1, S_MAX) for _ in range(500)],
            "все S от 1 до 120": list(range(1, S_MAX + 1))}
    for title, sums in sets.items():                    # две серии данных
        print(f"{title}\n{'Алгоритм':<28}{'среднее,%':>10}{'медиана,%':>10}{'макс,%':>10}{'оптимум':>11}")
        evaluate("Ж1: наибольший номинал", lambda s, c: greedy(s, c, True), sums)
        evaluate("Ж2: наименьший номинал", lambda s, c: greedy(s, c, False), sums)
        evaluate("Ж6: лучшее из двух", best_of_two, sums)
        evaluate("Ж6: перебор 1-й монеты", greedy_improved, sums)
        print()

    # --- Время работы при росте суммы ---
    print(f"{'S':>9}{'жадный, с':>14}{'ДП, с':>12}{'отношение':>12}")
    for s in [10 ** 3, 10 ** 4, 10 ** 5, 10 ** 6]:      # растущая размерность
        t0 = time.perf_counter(); greedy(s, COINS); t_g = time.perf_counter() - t0       # время жадного
        t0 = time.perf_counter(); coins_dp(s, COINS); t_dp = time.perf_counter() - t0    # время ДП
        print(f"{s:>9}{t_g:>14.7f}{t_dp:>12.4f}{t_dp / t_g:>12.0f}")

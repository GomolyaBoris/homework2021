import random

N = input("Введите количество рандомных чисел: ")
N = int(N)

# сортируем от нуля до n-1 с помощью Богосорт
def bogoSort(a):
    n = len(a)
    while (is_sorted(a) == False):
        shuffle(a)


# Делаем проверку
def is_sorted(a):
    n = len(a)
    for i in range(0, n - 1):
        if (a[i] > a[i + 1]):
            return False
    return True


def shuffle(a):
    n = len(a)
    for i in range(0, n):
        r = random.randint(0, n - 1)
        a[i], a[r] = a[r], a[i]

# даём переменной а количество N членов из промежутка от 0 до 1000
a = []
for i in range(N):
    a.append(random.randint(1, 1000))

bogoSort(a)
print("отсортировано: ")
for i in range(len(a)):
    print(a[i]),
import math

a = (input("Введите число: "))

try:
     b = int(a)
except:
    print("Введите натуральное число ")
    exit()

a = int(a)

numbers = []
flags = []
i = 2
while i <= a:
    numbers.append(i)
    flags.append(False)
    i += 1

idx = 0

while idx < a // 2:
    n = numbers[idx]
    i = idx + n
    while i < len(numbers):
        flags[i] = True
        i += n

    idx += 1
    while idx < len(flags) and flags[idx]:
        idx += 1

i = 0
while i < len(numbers):
    if flags[i]:
        i += 1
        continue
    print(numbers[i], end=" ")
    i += 1
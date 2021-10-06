import math

a = input("Введите целое число: ")

if float(a) % 1 != 0:
    print("Введите целое число")
    exit()

b = input("Введите второе целое число: ")

if float(b) % 1 != 0:
    print("Введите целое число")
    exit()

c = math.gcd(int(a), int(b))

print(c)

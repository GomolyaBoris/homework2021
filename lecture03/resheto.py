a = []
chislo = input("Введите целое число:  ")

if float(chislo) % 1 != 0:
    print("Вы ввели не натуральное число. Введите целое число, пожайлуста!")
    exit()


for i in range (2, int(chislo) + 1):
    k = 0
    for j in range(1, i + 1):
        if i % j == 0:
            k += 1
    if k == 2:
        a.append(i)

print(a)

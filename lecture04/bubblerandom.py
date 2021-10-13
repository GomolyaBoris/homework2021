from random import randint

def bubble(array):
    for i in range(N-1):
        for j in range(N-i-1):
            if array[j] > array[j+1]:
                buff = array[j]
                array[j] = array[j + 1]
                array[j + 1] = buff

N = input("Введите количество рандомных чисел: ")

try:
     b = int(N)
except:
    print("Введите натуральное число ")
    exit()

N = int(N)

a = []
for i in range(N):
    a.append(randint(1, 1000))

bubble(a)
print(a)
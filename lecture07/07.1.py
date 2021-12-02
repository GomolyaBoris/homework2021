class Operation:

    def plus(self, x, y):
        print(x + y)

    def minus(self, x, y):
        print(x - y)

    def multiplication(self, x, y):
        print(x * y)

    def division(self, x, y):
        print(x / y)

    def module(self, x, y):
        print(abs(3 + 4j))

    def degree(self, x, y):
        print(pow(x + y, 2))


obj1 = Operation()
x = complex(int(input("Введите первое значение для X: ")), int(input("Введите второе значение для X: ")))
y = complex(int(input("Введите первое значение для Y: ")), int(input("Введите второе значение для Y: ")))
print("Сложение:")
obj1.plus(x, y)
print("Разность:")
obj1.minus(x, y)
print("Произведение:")
obj1.multiplication(x, y)
print("Деление:")
obj1.division(x, y)
print("Модуль:")
obj1.module(x, y)
print("Возведение в степень:")
obj1.degree(x, y)
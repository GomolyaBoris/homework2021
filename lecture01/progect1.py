import math
a = float(input("Введите длину первой стороны треугольника: "))
b = float(input("Введите длину второй стороны треугольника: "))
c = float(input("Введите градус угла треугольника: "))

print(math.sqrt(a**2+b**2-2*a*b*math.cos(math.radians(c))))
from sympy import solveset, symbols, Interval, Min, Max
x = symbols('x')
#прописываем начало и конец отрезка
lower_bound = int(input("начало отрезка: "))
upper_bound = int(input("конец отрезка: "))
f = x**3 + 2*x**2 + 3*x + 1 #функция, которую можно поменять

#ищем минимум и максимум функции
zeros = solveset(f, x, domain=Interval(lower_bound, upper_bound))
assert zeros.is_FiniteSet
min = Min(f.subs(x, lower_bound), f.subs(x, upper_bound), *[f.subs(x, i) for i in zeros])
max = Max(f.subs(x, lower_bound), f.subs(x, upper_bound), *[f.subs(x, i) for i in zeros])

print('max: ', max )
print('min: ', min )
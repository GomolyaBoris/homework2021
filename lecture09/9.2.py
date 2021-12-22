import roman # да, из интернета


class Number:
    n = 0

    def __init__(self, numb):
        self.n = numb
        # только такая идея была
        self.bin = bin(self.n)
        self.hex = hex(self.n)
        self.dec = self.n
        self.roman = roman.write_roman(self.n)

    def __add__(self, other):
        if isinstance(other, Number):
            return Number(self.n + other.n)


n = Number(401)
n = n + Number(100)
print(n.dec)  # тут я не совсем понял, ибо мы передаем всегда десятичное число, но можно было бы доработать
print(n.bin)
print(n.hex)
print(n.roman)
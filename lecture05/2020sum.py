a = open('task1.txt', 'r')
a = a.readlines()
a = list(map(lambda x: str(x)[:-1], a))
a = [int(x) for x in a]
res = []

for x in a:
    for y in a:
        for z in a:
            if (x + y + z) == 2020:
                res.append(x * y * z)
res = list(set(res))
print("Откройте файл output:", *res)


with open('task1_output.txt', 'w') as file:
    for x in res:
        file.write(str(x))
        file.write('\n')
file.close()
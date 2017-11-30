import random, datetime


def gerar_codigo():
    result = random.sample(range(10, 100), 2)

    cod = ''

    for i in result:
        cod += str(i)

    cod = int(cod)
    return cod

print(datetime.datetime.now().second)
print(datetime.datetime.now().second + 30)


